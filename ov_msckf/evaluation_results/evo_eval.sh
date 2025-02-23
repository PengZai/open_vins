
DATASET="BotanicGarden"
DIR="1005_07"

ESITMATED_FOLDER="openvins_stereo_inertial_${DIR}_img10hz600p"
REFERENCE="${DIR}_GT_output.txt"

evo_rpe tum $DATASET/$DIR/${ESITMATED_FOLDER}/${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.txt $DATASET/$DIR/$REFERENCE  > $DATASET/$DIR/${ESITMATED_FOLDER}/rpe_${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.log
evo_ape tum $DATASET/$DIR/${ESITMATED_FOLDER}/${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.txt $DATASET/$DIR/$REFERENCE  > $DATASET/$DIR/${ESITMATED_FOLDER}/ape_${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.log
evo_ape tum $DATASET/$DIR/${ESITMATED_FOLDER}/${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.txt $DATASET/$DIR/$REFERENCE --align --pose_relation trans_part > $DATASET/$DIR/${ESITMATED_FOLDER}/ate_${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.log


evo_traj tum $DATASET/$DIR/${ESITMATED_FOLDER}/${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.txt --ref=$DATASET/$DIR/$REFERENCE -p --plot_mode=xyz --save_plot $DATASET/$DIR/${ESITMATED_FOLDER}/3d  
evo_traj tum $DATASET/$DIR/${ESITMATED_FOLDER}/${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.txt --ref=$DATASET/$DIR/$REFERENCE -p --plot_mode=xy --save_plot $DATASET/$DIR/${ESITMATED_FOLDER}/2d 
