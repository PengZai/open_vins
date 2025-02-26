import os
import numpy as np 
from evo.tools import file_interface
from evo.core.trajectory import PoseTrajectory3D
import shutil

# Define the input and output filenames
sequence_name = '1005_07'
sensor_type = 'monocular_inertial'
filename_prefix = '_'.join(['openvins', sensor_type, 'for', sequence_name, 'img10hz600p'])
openvins_estimated_surffix = 'traj_estimate'
openvins_timing_surffix = 'traj_timing'

if not os.path.exists(os.path.join(sequence_name, filename_prefix)):
    os.makedirs(os.path.join(sequence_name, filename_prefix))

testfolder_names = [f for f in os.listdir(os.path.join(sequence_name, filename_prefix))]
current_testfolder_name = '_'.join(['test', str(len(testfolder_names))])
if not os.path.exists(os.path.join(sequence_name, filename_prefix, current_testfolder_name)):
    os.makedirs(os.path.join(sequence_name, filename_prefix, current_testfolder_name))
if not os.path.exists(os.path.join(sequence_name, filename_prefix, current_testfolder_name, 'config')):
    os.makedirs(os.path.join(sequence_name, filename_prefix, current_testfolder_name, 'config'))    



# Open the input file for reading and the output file for writing
with open(os.path.join(sequence_name, '_'.join([filename_prefix, openvins_estimated_surffix+'.txt'])), 'r') as infile, open(os.path.join(sequence_name, filename_prefix, current_testfolder_name, '_'.join([filename_prefix, openvins_estimated_surffix, 'tum_format.txt'])), 'w') as outfile:
    # Process each line in the input file
    for line in infile:
        # Remove leading/trailing whitespace
        stripped_line = line.strip()
        # Skip empty lines
        if not stripped_line:
            continue
        # Split the line into tokens based on whitespace
        tokens = stripped_line.split()
        # Select the first eight tokens
        first_eight = tokens[:8]
        # Join the tokens back into a single string
        new_line = ' '.join(first_eight)
        # Write the new line to the output file
        outfile.write(new_line + '\n')

shutil.copy(os.path.join(sequence_name, '_'.join([filename_prefix, openvins_estimated_surffix+".txt"])), os.path.join(sequence_name, filename_prefix, current_testfolder_name, '_'.join([filename_prefix, openvins_estimated_surffix+'.txt'])))
shutil.copy(os.path.join(sequence_name, '_'.join([filename_prefix, openvins_timing_surffix+".txt"])), os.path.join(sequence_name, filename_prefix, current_testfolder_name, '_'.join([filename_prefix, openvins_timing_surffix+'.txt'])))
shutil.copytree(os.path.join('../../../config', 'BotanicGarden'), os.path.join(sequence_name, filename_prefix, current_testfolder_name, 'config', 'BotanicGarden'))



# because KeyFrame is in Xsens coordinates, so we need to transfer it to RGB0 coordinates
# RGB0 in Xsens coordinates
sensor_coordinate_transform_matrix_for_camera_frame = np.array([
    [0.999678872580465,0.0252865664429322,0.00150422292234868,0],  
    [-0.0252723438960774,0.999649431893338,-0.0078025434141585,0],  
    [-0.00170103929405540,0.00776298237926191,0.99996789371916,0],  
    [0.0,0.0,0.0,1.0]
])

# seems x in key frame of orbslam system is -z in BotanicGarden
system_coordinate_transform_matrix_for_camera_frame = np.array([
    [0., -1.,   0.,  0],  
    [1., 0.,   0.,  0],  
    [0., 0.,   1.,  0],  
    [0., 0,    0,   1.0]
])

# system_coordinate_transform_matrix_for_camera_frame = np.array([
#     [1., 0.,   0.,  0],  
#     [0., 1.,   0.,  0],  
#     [0., 0.,   1.,  0],  
#     [0., 0,    0,   1.0]
# ])

def invert_transformation_matrix(T):
    """
    Computes the inverse of a 4x4 homogeneous transformation matrix.
    
    Parameters:
        T (numpy.ndarray): 4x4 transformation matrix
    
    Returns:
        numpy.ndarray: 4x4 inverse transformation matrix
    """
    # Extract rotation (R) and translation (t)
    R = T[:3, :3]  # 3x3 rotation matrix
    t = T[:3, 3]   # 3x1 translation vector

    # Compute the inverse transformation
    R_inv = R.T  # Transpose of rotation matrix
    t_inv = -R_inv @ t  # Compute new translation

    # Construct the inverse transformation matrix
    T_inv = np.eye(4)
    T_inv[:3, :3] = R_inv
    T_inv[:3, 3] = t_inv

    return T_inv



traj = file_interface.read_tum_trajectory_file(open(os.path.join(sequence_name, filename_prefix, current_testfolder_name, '_'.join([filename_prefix, openvins_estimated_surffix, 'tum_format.txt']))))

transformed_poses = []
for pose in traj.poses_se3:

    # Tvi * Tib
    transformed_pose_matrix = system_coordinate_transform_matrix_for_camera_frame @ invert_transformation_matrix(sensor_coordinate_transform_matrix_for_camera_frame) @ pose

    # Append transformed pose as SE3 object
    transformed_poses.append(transformed_pose_matrix)

traj = PoseTrajectory3D(
    poses_se3=transformed_poses,
    timestamps=traj.timestamps
)

file_interface.write_tum_trajectory_file(os.path.join(sequence_name, filename_prefix, current_testfolder_name, '_'.join([filename_prefix, openvins_estimated_surffix, 'coordinate_aligned.txt'])), traj)