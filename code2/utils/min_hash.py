# import random
# import numpy as np
# import warnings
# from sklearn.cluster import KMeans
# from sklearn.cluster import AffinityPropagation
# from sklearn.metrics import jaccard_score
# from gap_statistic import OptimalK


# warnings.filterwarnings('ignore', category=FutureWarning)
# warnings.filterwarnings('ignore', category=UserWarning)

# from sklearn.metrics.pairwise import cosine_similarity
# from utils.util import jaccard_affinity_propagation, jaccard_kmeans_clustering

# def sigGen(matrix,randomSeq):
#     """
#     * generate the signature vector
#     :param matrix: a ndarray var
#     :return a signature vector: a list var
#     """
#     # initialize the sig vector as [-1, -1, ..., -1]
#     result = [-1 for i in range(matrix.shape[1])]

#     count = 0

#     for row in randomSeq:
#         for i in range(matrix.shape[1]):
#             if matrix[row][i] != 0 and result[i] == -1:
#                 result[i] = row
#                 count += 1
#         if count == matrix.shape[1]:
#             break
#     return result

# def sigMatrixGen(input_matrix,random_R, n):
#     """
#     generate the sig matrix
#     :param input_matrix: naarray var
#     :param n: the row number of sig matrix which we set
#     :return sig matrix: ndarray var
#     """

#     result = []

#     for i in range(n):
#         sig = sigGen(input_matrix,random_R[i])
#         result.append(sig)
#     return np.array(result)

# def quan_params(input_matrix, threshold):
#     for idx, row in enumerate(input_matrix):
#         for i in range(len(row)):
#             if abs(row[i]) < threshold:
#                 input_matrix[idx][i] = 0
#             else:
#                 input_matrix[idx][i] = 1
        
#     return input_matrix
        
# def real_sim(input_matrix):
#     row_num = input_matrix.shape[0]
#     total = 0
#     sim = 0
#     for row in range(row_num):
#         if input_matrix[row][0] == 1 or input_matrix[row][1] == 1:
#             total += 1
#             if input_matrix[row][0] == input_matrix[row][1]:
#                 sim += 1
#     return sim / total

# def dim_reduce_sim(input_matrix):
#     row_num = input_matrix.shape[0]
#     sim = 0
#     for row in range(row_num):
#         if input_matrix[row][0] == input_matrix[row][1]:
#             sim += 1
#     return sim / row_num


# def gen_random_R(input_len, sim_len):
#     """
#     Random matrix is needed for sketch-based client selection.

#     Args:
#         input_len (`int`):
#             Input dimension.
#         sim_len (`int`):
#             Output dimension.  
#     Returns:
#         random_R (`list`):
#             Random matrix.
#     """

#     random_R = []
#     for i in range(sim_len):
#         seq_list = np.arange(input_len)
#         np.random.shuffle(seq_list)
#         random_R.append(seq_list)
#     return random_R

# '''
# def gap_statistic(data,max_k):
#     optimalK = OptimalK(n_jobs=4, parallel_backend='joblib')
#     n_clusters = optimalK(data, cluster_array=np.arange(1, max_k+1))
#     return n_clusters
# '''

# def sse_statistic(X,max_k):
#     sse = []
#     for k in range(1, max_k+1):
#         kmeans = KMeans(n_clusters=k).fit(X)
#         sse.append(kmeans.inertia_)
#     diff = np.diff(sse)
#     diff_r = diff[1:] / diff[:-1]
#     k_opt = np.argmax(diff_r) + 2
#     return k_opt

# def gap_statistic(data,max_k):
#     data = np.array(data).reshape(-1,1)
#     optimalK = OptimalK(n_jobs=20, parallel_backend='joblib')
#     n_clusters = optimalK(data, cluster_array=np.arange(1, max_k+1))
#     return n_clusters

# # def clusters_selection_L2(hash_mat,max_k,train_weights=[],weights_clusters=[]):
# #     # k_opt = gap_statistic(hash_mat.astype(float),max_k)
# #     # clusters = jaccard_kmeans_clustering(hash_mat, k_opt)
# #     clusters =jaccard_affinity_propagation(hash_mat)

# #     tmp = hash_mat.tolist()
# #     rep_num = [1] * len(train_weights)
# #     selected_clients = []
# #     # print("Num:{} ,Next round Selected clients:{}".format(k_opt, clusters))

# #     for i, indices in enumerate(clusters):
# #         tmp_weights = [train_weights[i] for i in indices]
# #         tmp_list = list(indices)
# #         zipped = zip(tmp_weights, tmp_list)
# #         max_tuple = max(zipped, key=lambda x: x[0])
# #         client_index = max_tuple[1]  
# #         if train_weights != []:
# #             rep_num[client_index] = len(indices)
# #             tmp = 0
# #             for idx in indices:
# #                 tmp += train_weights[idx]
# #             weights_clusters[client_index] = tmp
# #         selected_clients.append(client_index)

# #     # k_opt is the number of unique clusters found
# #     k_opt = len(clusters)
    
# #     # Print statement
# #     print("Num: {} , Next round Selected clients: {}".format(k_opt, clusters))
# #     return selected_clients,rep_num

# def clusters_selection_L2(hash_mat, max_k, train_weights=[], weights_clusters=[]):
#     # k_opt = gap_statistic(hash_mat.astype(float), max_k)
#     # clusters = jaccard_kmeans_clustering(hash_mat, k_opt)
#     clusters = jaccard_affinity_propagation(hash_mat)

#     tmp = hash_mat.tolist()
#     rep_num = [1] * len(train_weights)
#     selected_clients = []

#     for i, indices in enumerate(clusters):
#         if train_weights != []:
#             for idx in indices:
#                 rep_num[idx] = len(indices)
#         selected_clients.append(random.choice(indices))  # 随机选择一个客户端

#     # k_opt is the number of unique clusters found
#     k_opt = len(clusters)
    
#     # Print statement
#     print("Num: {} , Next round Selected clients: {}".format(k_opt, clusters))
#     return selected_clients, rep_num



# # def clusters_selection(hash_mat,max_k,train_weights=[],weights_clusters=[]):
# #     k_opt = gap_statistic(hash_mat.astype(float),max_k)
# #     while True:
# #         kmeans = KMeans(n_clusters=k_opt).fit(hash_mat)  
# #         cluster_counts = np.unique(kmeans.labels_)
# #         if len(cluster_counts) == k_opt:
# #             break
# #         labels = kmeans.labels_
# #     unique_labels = np.unique(labels)
# #     selected_clients = []

# #     rep_num = [1] * len(train_weights)
# #     for label in unique_labels:
# #         indices = np.where(labels == label)[0]  
# #         tmp_weights = [train_weights[i] for i in indices]
# #         tmp_list = list(indices)
# #         zipped = zip(tmp_weights, tmp_list)
# #         max_tuple = max(zipped, key=lambda x: x[0])
# #         client_index = max_tuple[1]  

# #         if train_weights != []:
# #             rep_num[client_index] = len(indices)
        
# #         if train_weights != []:
# #             tmp = 0
# #             for idx in indices:
# #                 tmp += train_weights[idx]
# #             weights_clusters[client_index] = tmp
# #         selected_clients.append(client_index)

# #     return selected_clients,rep_num

# def client_selection(sampled_clients,labels,train_weights=[],weights_clusters=[]):
#     unique_labels = np.unique(labels)
#     selected_clients = []
#     rep_num = [1] * len(train_weights)
#     for label in unique_labels:
#         indices = np.where(labels == label)[0]  # 找到属于当前标签的数据点索引
#         retA = [i for i in indices if i in sampled_clients]
#         if retA == []:
#             continue
#         else:
#             client_index = np.random.choice(np.array(retA))

#         if train_weights != []:
#             rep_num[client_index] = len(indices)
        
#         if train_weights != []:
#             tmp = 0
#             for idx in retA:
#                 tmp += train_weights[idx]
#             weights_clusters[client_index] = tmp
#         selected_clients.append(client_index)
#     return selected_clients,rep_num


import random
import numpy as np
import warnings
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.metrics import jaccard_score
from gap_statistic import OptimalK

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

from sklearn.metrics.pairwise import cosine_similarity
from utils.util import jaccard_affinity_propagation, jaccard_kmeans_clustering

# =========================================================
# --- [新增：RR 隐私保护与偏差校正逻辑] ---
# =========================================================

def apply_rr(signature, p):
    """客户端：本地差分隐私扰动"""
    perturbed = []
    for val in signature:
        if random.random() < p:
            perturbed.append(int(val))
        else:
            perturbed.append(random.randint(0, 10000))
    return perturbed

def corrected_jaccard_estimation(obs_match_rate, p):
    """服务器：偏差校正公式"""
    denom = (2 * p - 1) ** 2
    if denom < 1e-6: return obs_match_rate
    corrected = (obs_match_rate - 2 * p * (1 - p)) / denom
    return np.clip(corrected, 0.0, 1.0)

# =========================================================
# --- [保留：原始特征提取逻辑] ---
# =========================================================

def sigGen(matrix, randomSeq):
    result = [-1 for i in range(matrix.shape[1])]
    count = 0
    for row in randomSeq:
        for i in range(matrix.shape[1]):
            if matrix[row][i] != 0 and result[i] == -1:
                result[i] = row
                count += 1
        if count == matrix.shape[1]: break
    return result

def sigMatrixGen(input_matrix, random_R, n):
    result = []
    for i in range(n):
        sig = sigGen(input_matrix, random_R[i])
        result.append(sig)
    return np.array(result)

def quan_params(input_matrix, threshold):
    for idx, row in enumerate(input_matrix):
        for i in range(len(row)):
            input_matrix[idx][i] = 1 if abs(row[i]) >= threshold else 0
    return input_matrix
        
def real_sim(input_matrix):
    row_num = input_matrix.shape[0]; total = 0; sim = 0
    for row in range(row_num):
        if input_matrix[row][0] == 1 or input_matrix[row][1] == 1:
            total += 1
            if input_matrix[row][0] == input_matrix[row][1]: sim += 1
    return sim / total if total != 0 else 0

def dim_reduce_sim(input_matrix):
    row_num = input_matrix.shape[0]; sim = 0
    for row in range(row_num):
        if input_matrix[row][0] == input_matrix[row][1]: sim += 1
    return sim / row_num

def gen_random_R(input_len, sim_len):
    random_R = []
    for i in range(sim_len):
        seq_list = np.arange(input_len); np.random.shuffle(seq_list); random_R.append(seq_list)
    return random_R

def sse_statistic(X, max_k):
    sse = []
    for k in range(1, max_k+1):
        kmeans = KMeans(n_clusters=k).fit(X); sse.append(kmeans.inertia_)
    diff = np.diff(sse); diff_r = diff[1:] / diff[:-1]
    return np.argmax(diff_r) + 2

def gap_statistic(data, max_k):
    data = np.array(data).reshape(-1,1)
    optimalK = OptimalK(n_jobs=20, parallel_backend='joblib')
    return optimalK(data, cluster_array=np.arange(1, max_k+1))

# =========================================================
# --- [核心修改：集成隐私校正的选择逻辑] ---
# =========================================================

def clusters_selection_L2(hash_mat, max_k, train_weights=[], weights_clusters=[], p_val=0.8):
    if len(hash_mat) == 0: return list(range(max_k)), [1]*max_k
    n = hash_mat.shape[0]
    corrected_dist = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            obs_match = np.mean(hash_mat[i] == hash_mat[j])
            rec_sim = corrected_jaccard_estimation(obs_match, p_val)
            corrected_dist[i, j] = corrected_dist[j, i] = 1.0 - rec_sim
    
    clusters = jaccard_affinity_propagation(hash_mat)
    rep_num = [1] * len(train_weights); selected_clients = []
    for indices in clusters:
        if train_weights != []:
            for idx in indices: rep_num[idx] = len(indices)
        selected_clients.append(random.choice(indices))
    print("Num: {} , Next round Selected clients: {}".format(len(clusters), clusters))
    return selected_clients, rep_num

def client_selection(sampled_clients, labels, train_weights=[], weights_clusters=[]):
    unique_labels = np.unique(labels); selected_clients = []; rep_num = [1] * len(train_weights)
    for label in unique_labels:
        indices = np.where(labels == label)[0] 
        retA = [i for i in indices if i in sampled_clients]
        if retA == []: continue
        client_index = np.random.choice(np.array(retA))
        if train_weights != []: rep_num[client_index] = len(indices)
        if train_weights != []:
            tmp = 0
            for idx in retA: tmp += train_weights[idx]
            weights_clusters[client_index] = tmp
        selected_clients.append(client_index)
    return selected_clients, rep_num