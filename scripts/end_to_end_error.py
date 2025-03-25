START_ODOM_POSITION = [0, 0, 0] # x, y, z
START_ODOM_ORIENTATION = [0, 0, 0, 1] # x, y, z, w

# genz-icp
# END_ODOM_POSITION = [0.008543130564488789,
#                      0.009166975099478841,
#                      0.0032279790139008134]
# END_ODOM_ORIENTATION = [0.0018088269005035352,
#                         9.100110566791067e-05,
#                         0.003530531453309538,
#                         -0.9999921275748624]

# kiss-icp
END_ODOM_POSITION = [1.173197100685434,
                     0.762363780819155,
                     -0.2062488847693311]
END_ODOM_ORIENTATION = [-0.09840242881281337,
                        0.001085688963711003,
                        -0.11828287228652795,
                        -0.9880915673189717]

# =====================================================================================

import numpy as np
from tf.transformations import quaternion_inverse, quaternion_multiply, euler_from_quaternion

def compute_translation_error(gt_pos, est_pos):
    error = np.array(est_pos) - np.array(gt_pos)
    rmse = np.linalg.norm(error)
    return rmse, error

def compute_rotation_error(gt_ori, est_ori):
    # rotation difference: q_error = est * gt_inv
    q_error = quaternion_multiply(est_ori, quaternion_inverse(gt_ori))
    roll, pitch, yaw = euler_from_quaternion(q_error)

    error_rad = np.array([roll, pitch, yaw])
    rmse = np.linalg.norm(error_rad)
    return rmse, error_rad

def compute_ape_6dof(gt_pos, gt_ori, est_pos, est_ori):
    trans_rmse, trans_error = compute_translation_error(gt_pos, est_pos)
    rot_rmse, rot_error_rad = compute_rotation_error(gt_ori, est_ori)

    print("=== APE (6DoF) Results ===")
    print(f"Translation Error: {trans_rmse:.4f} m")
    print(f" → Vector Error: {trans_error}")
    print(f"Rotation Error: {rot_rmse:.4f} rad")
    print(f" → Roll: {rot_error_rad[0]:.4f}, Pitch: {rot_error_rad[1]:.4f}, Yaw: {rot_error_rad[2]:.4f}")


if __name__ == "__main__":

    compute_ape_6dof(START_ODOM_POSITION,START_ODOM_ORIENTATION,END_ODOM_POSITION,END_ODOM_ORIENTATION)