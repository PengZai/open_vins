
DATASET="BotanicGarden"
DIR="1005_07"
TEST_DIR="test_0"
ESITMATED_FOLDER="openvins_monocular_inertial_for_${DIR}_img10hz600p"
REFERENCE="${DIR}_GT_output.txt"

evo_rpe tum $DATASET/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.txt $DATASET/$DIR/$REFERENCE --plot_mode=xy --save_plot ${DATASET}/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/2d_rpe_traj_estimate > $DATASET/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/rpe_${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.log
evo_ape tum $DATASET/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.txt $DATASET/$DIR/$REFERENCE --plot_mode=xy --save_plot ${DATASET}/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/2d_ape_traj_estimate > $DATASET/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/ape_${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.log
evo_ape tum $DATASET/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.txt $DATASET/$DIR/$REFERENCE --align --pose_relation trans_part --plot_mode=xy --save_plot ${DATASET}/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/2d_ate_traj_estimate > $DATASET/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/ate_${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.log


evo_traj tum $DATASET/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.txt --ref=$DATASET/$DIR/$REFERENCE -p --plot_mode=xyz --save_plot $DATASET/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/3d  
evo_traj tum $DATASET/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/${ESITMATED_FOLDER}_traj_estimate_coordinate_aligned.txt --ref=$DATASET/$DIR/$REFERENCE -p --plot_mode=xy --save_plot $DATASET/$DIR/${ESITMATED_FOLDER}/${TEST_DIR}/2d 
