import abc
import logging
import torch
import torch.nn.functional as F
import numpy as np
from inclearn.tools.metrics import ClassErrorMeter

LOGGER = logging.Logger("IncLearn", level="INFO")


class IncrementalLearner(abc.ABC):
    
    """Base incremental learner.

    Methods are called in this order (& repeated for each new task):

    1. set_task_info
    2. before_task
    3. train_task
    4. after_task
    5. eval_task
    """
    def __init__(self, *args, **kwargs):
        self._increments = []
        self._seen_classes = []

    def set_task_info(self, task, total_n_classes, increment, n_train_data, n_test_data, n_tasks):
        # 初始化任务信息
        self._task = task
        self._task_size = increment
        self._increments.append(self._task_size)
        self._total_n_classes = total_n_classes
        self._n_train_data = n_train_data
        self._n_test_data = n_test_data
        self._n_tasks = n_tasks

    def before_task(self, taski, inc_dataset):
        LOGGER.info("Before task")
        self.eval()
        self._before_task(taski, inc_dataset)

    def train_task(self, train_loader, val_loader):
        LOGGER.info("train task")
        self.train() # 设置为 train 模式 ，如果使用 DER ，则分别设置 eval 和 train 模式
        self._train_task(train_loader, val_loader)

    def after_task(self, taski, inc_dataset):
        LOGGER.info("after task")
        self.eval()
        self._after_task(taski, inc_dataset)

    def eval_task(self, data_loader):
        LOGGER.info("eval task")
        self.eval()
        return self._eval_task(data_loader)

    def get_memory(self):
        return None

    def eval(self):
        raise NotImplementedError

    def train(self):
        raise NotImplementedError

    def _before_task(self, data_loader):
        pass

    def _train_task(self, train_loader, val_loader):
        raise NotImplementedError

    def _after_task(self, data_loader):
        pass

    def _eval_task(self, data_loader):
        raise NotImplementedError

    @property
    def _new_task_index(self):
        return self._task * self._task_size

    @property
    def _memory_per_class(self):
        """Returns the number of examplars per class."""
        return self._memory_size.mem_per_cls

    def _after_epoch(self, epoch, avg_loss, train_new_accu, train_old_accu, accu):
        self._run.log_scalar(f"train_loss_trial{self._trial_i}_task{self._task}", avg_loss, epoch + 1)
        self._tensorboard.add_scalar(f"trial{self._trial_i}_task{self._task}/train_loss", avg_loss, epoch + 1)

        # self._run.log_scalar(f"train_new_accu_trial{self._trial_i}_task{self._task}",
        #                      train_new_accu.value()[0], epoch + 1)
        # self._tensorboard.add_scalar(f"trial{self._trial_i}_task{self._task}/train_new_accu",
        #                              train_new_accu.value()[0], epoch + 1)

        # if self._task != 0:
        #     self._run.log_scalar(f"train_old_accu_trial{self._trial_i}_task{self._task}",
        #                          train_old_accu.value()[0], epoch + 1)
        #     self._tensorboard.add_scalar(f"trial{self._trial_i}_task{self._task}/train_old_accu",
        #                                  train_old_accu.value()[0], epoch + 1)

        self._run.log_scalar(f"train_accu_trial{self._trial_i}_task{self._task}", accu.value()[0], epoch + 1)
        self._tensorboard.add_scalar(f"trial{self._trial_i}_task{self._task}/train_accu", accu.value()[0], epoch + 1)
        # self._tensorboard.close()
        self._tensorboard.flush()

    def _validation(self, val_loader, epoch):
        topk = 5 if self._n_classes >= 5 else self._n_classes
        if self._val_per_n_epoch != -1 and epoch % self._val_per_n_epoch == 0:
            _val_loss = 0
            _val_accu = ClassErrorMeter(accuracy=True, topk=[1, topk])
            _val_new_accu = ClassErrorMeter(accuracy=True)
            _val_old_accu = ClassErrorMeter(accuracy=True)
            self._parallel_network.eval()
            with torch.no_grad():
                for i, (inputs, targets) in enumerate(val_loader, 1):
                    old_classes = targets < (self._n_classes - self._task_size)
                    new_classes = targets >= (self._n_classes - self._task_size)
                    val_loss, _ = self._forward_loss(
                        inputs,
                        targets,
                        old_classes,
                        new_classes,
                        accu=_val_accu,
                        old_accu=_val_old_accu,
                        new_accu=_val_new_accu,
                    )
                    _val_loss += val_loss.item()
            self._ex.logger.info(
                f"epoch{epoch} val acc:{_val_accu.value()[0]:.2f}, val top5acc:{_val_accu.value()[1]:.2f}")
            # Test accu
            self._run.log_scalar(f"test_accu_trial{self._trial_i}_task{self._task}", _val_accu.value()[0], epoch + 1)
            self._run.log_scalar(f"test_5accu_trial{self._trial_i}_task{self._task}", _val_accu.value()[1], epoch + 1)
            self._tensorboard.add_scalar(f"trial{self._trial_i}_task{self._task}/test_accu",
                                         _val_accu.value()[0], epoch + 1)
            self._tensorboard.add_scalar(f"trial{self._trial_i}_task{self._task}/test_5accu",
                                         _val_accu.value()[1], epoch + 1)

            # Test new accu
            self._run.log_scalar(f"test_new_accu_trial{self._trial_i}_task{self._task}",
                                 _val_new_accu.value()[0], epoch + 1)
            self._tensorboard.add_scalar(f"trial{self._trial_i}_task{self._task}/test_new_accu",
                                         _val_new_accu.value()[0], epoch + 1)

            # Test old accu
            if self._task != 0:
                self._run.log_scalar(f"test_old_accu_trial{self._trial_i}_task{self._task}",
                                     _val_old_accu.value()[0], epoch + 1)
                self._tensorboard.add_scalar(f"trial{self._trial_i}_task{self._task}/test_old_accu",
                                             _val_old_accu.value()[0], epoch + 1)

            # Test loss
            self._run.log_scalar(f"test_loss_trial{self._trial_i}_task{self._task}", round(_val_loss / i, 3), epoch + 1)
            self._tensorboard.add_scalar(f"trial{self._trial_i}_task{self._task}/test_loss", round(_val_loss / i, 3),
                                         epoch + 1)
            self._tensorboard.close()