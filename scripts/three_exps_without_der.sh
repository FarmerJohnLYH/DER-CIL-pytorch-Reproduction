name='B0S10_noder'
comments='None'
expid='B0S10_noder'
    python -m main train with "./configs/${expid}.yaml" \
    exp.name="${name}" \
    exp.savedir="./logs/" \
    exp.ckptdir="./logs/" \
    exp.tensorboard_dir="./tensorboard/" \
    exp.debug=False \
    --name="${name}" \
    -D \
    -p \
    --force 


# name='B0S5_noder'
# comments='None'
# expid='B0S5_noder'
#     python -m main train with "./configs/${expid}.yaml" \
#     exp.name="${name}" \
#     exp.savedir="./logs/" \
#     exp.ckptdir="./logs/" \
#     exp.tensorboard_dir="./tensorboard/" \
#     exp.debug=True \
#     --name="${name}" \
#     -D \
#     -p \
#     --force 

# name='B50S10_noder'
# comments='None'
# expid='B50S10_noder'
#     python -m main train with "./configs/${expid}.yaml" \
#     exp.name="${name}" \
#     exp.savedir="./logs/" \
#     exp.ckptdir="./logs/" \
#     exp.tensorboard_dir="./tensorboard/" \
#     exp.debug=True \
#     --name="${name}" \
#     -D \
#     -p \
#     --force 