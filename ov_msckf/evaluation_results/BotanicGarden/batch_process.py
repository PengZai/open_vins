import os
import numpy as np 
from evo.tools import file_interface
from evo.core.trajectory import PoseTrajectory3D
import shutil

# Define the input and output filenames
folder = '1005_07'
filename_prefix = 'openvins_stereo_inertial_1005_07_img10hz600p'
openvins_estimated_surffix = 'traj_estimate'
openvins_timing_surffix = 'traj_timing'


if not os.path.exists(os.path.join(folder, filename_prefix)):
    os.makedirs(os.path.join(folder, filename_prefix))

# Open the input file for reading and the output file for writing
with open(os.path.join(folder, '_'.join([filename_prefix, openvins_estimated_surffix+'.txt'])), 'r') as infile, open(os.path.join(folder, filename_prefix, '_'.join([filename_prefix, openvins_estimated_surffix, 'tum_format.txt'])), 'w') as outfile:
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

shutil.copy(os.path.join(folder, '_'.join([filename_prefix, openvins_estimated_surffix+'.txt'])), os.path.join(folder, filename_prefix, '_'.join([filename_prefix, openvins_estimated_surffix+'.txt'])))
shutil.copy(os.path.join(folder, '_'.join([filename_prefix, openvins_timing_surffix+'.txt'])), os.path.join(folder, filename_prefix, '_'.join([filename_prefix, openvins_timing_surffix+'.txt'])))



# because KeyFrame is in Xsens coordinates, so we need to transfer it to RGB0 coordinates
# RGB0 in Xsens coordinates
sensor_coordinate_transform_matrix_for_camera_frame = np.array([
    [1., 0.,   0.,  0],  
    [0., 1.,   0.,  0],  
    [0., 0.,   1.,  0],  
    [0., 0,    0,   1.0]
])

# seems x in key frame of orbslam system is -z in BotanicGarden
system_coordinate_transform_matrix_for_camera_frame = np.array([
    [0., -1.,   0.,  0],  
    [1., 0.,   0.,  0],  
    [0., 0.,   1.,  0],  
    [0., 0,    0,   1.0]
])

traj = file_interface.read_tum_trajectory_file(open(os.path.join(folder, filename_prefix, '_'.join([filename_prefix, openvins_estimated_surffix, 'tum_format.txt']))))

transformed_poses = []
for pose in traj.poses_se3:

    
    transformed_pose_matrix =   system_coordinate_transform_matrix_for_camera_frame @ sensor_coordinate_transform_matrix_for_camera_frame @ pose

    # Append transformed pose as SE3 object
    transformed_poses.append(transformed_pose_matrix)

traj = PoseTrajectory3D(
    poses_se3=transformed_poses,
    timestamps=traj.timestamps
)

file_interface.write_tum_trajectory_file(os.path.join(folder, filename_prefix, '_'.join([filename_prefix, openvins_estimated_surffix, 'coordinate_aligned.txt'])), traj)