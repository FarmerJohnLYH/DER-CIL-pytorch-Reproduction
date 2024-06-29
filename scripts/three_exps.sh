# name='B0S5'
# comments='None'
# expid='B0S5'
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
name='B0S10'
comments='None'
expid='B0S10'
    python -m main train with "./configs/${expid}.yaml" \
    exp.name="${name}" \
    exp.savedir="./logs/" \
    exp.ckptdir="./logs/" \
    exp.tensorboard_dir="./tensorboard/" \
    exp.debug=True \
    --name="${name}" \
    -D \
    -p \
    --force 

name='B50S10'
comments='None'
expid='B50S10'
    python -m main train with "./configs/${expid}.yaml" \
    exp.name="${name}" \
    exp.savedir="./logs/" \
    exp.ckptdir="./logs/" \
    exp.tensorboard_dir="./tensorboard/" \
    exp.debug=True \
    --name="${name}" \
    -D \
    -p \
    --force 
    
    