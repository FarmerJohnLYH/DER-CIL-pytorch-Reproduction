
## DER.CIL.Pytorch.Reproduction
这个项目是 lyh 和 xzz 的《机器学习》课程大作业，完成了对 [DER: Dynamically Expandable Representation for Class Incremental Learning](http://arxiv.org/abs/2103.16788)（CVPR 2021）的论文复现，其中包括我们的.yaml和脚本，以及一些中文注释、实验结果。

本复现项目属于 [DER-ClassIL.pytorch](https://github.com/Rhyssiyan/DER-ClassIL.pytorch) 的一个分支。

## 数据集
* ImageNet100
* Cifar100

## 运行实验 
* 切换到相应的目录并运行以下命令
```
sh scripts/three_exps.sh
sh scripts/three_exps_without_der.sh
```
第一个脚本包括“Base-0,Inc-5”等三种增量学习策略。
第二个脚本是不使用 der 的运行脚本，用于测试 der 对性能的提升。

## 主要内容
1. **Docx_with_Annotations**
包含撰写的实验报告和PPT。
2. **Charts**
包含了在 PPT 中用到的大部分原始的数据的表格。
3. **configs**
包含参数配置。
4. **scripts**
复现论文所用的脚本。
