from matplotlib.mlab import PCA
import numpy as np
from sklearn.neighbors import NearestNeighbors

def pca_dim_reduction(input_data, target_dim):
    reduced_dataset = []
    # pca_obj = PCA(np.array(input_data))
    pca_obj = PCA(np.array(input_data), standardize=False)
    projected_dataset = pca_obj.Y.tolist()
    for projected_data in projected_dataset:
        reduced_data = []  # one data point with reduced dim
        for col in range(0, target_dim):
            reduced_data.append(projected_data[col])
        reduced_dataset.append(reduced_data)
    return reduced_dataset


# def get_trustworthiness(reduced_dataset, original_dataset, k):
#     rank_sum = 0
#     n = len(reduced_dataset)
#     for i in range(0, n):
#         curr_point = reduced_dataset[i]
#         curr_point_neib_ranking = sorted(reduced_dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(curr_point)), reverse=False)
#         curr_point_neib_ranking_mapping = dict()
#         for i_2 in range(1, n):
#             curr_point_neib_ranking_mapping[str(curr_point_neib_ranking[i_2])] = i_2
#         original_curr_point = original_dataset[i]
#         original_curr_point_neib_ranking = sorted(original_dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(original_curr_point)), reverse=False)
#         original_curr_point_neib_ranking_mapping = dict()
#         for i_2 in range(1, n):
#             original_curr_point_neib_ranking_mapping[str(original_curr_point_neib_ranking[i_2])] = i_2
#         for j in range(0, n):
#             if i == j:
#                 continue
#             # reduced_rank = get_rank(curr_point, reduced_dataset[j], reduced_dataset)
#             # reduced_rank = curr_point_neib_ranking.index(reduced_dataset[j])
#             reduced_rank = curr_point_neib_ranking_mapping[str(reduced_dataset[j])]
#             # original_rank = get_rank(original_curr_point, original_dataset[j], original_dataset)
#             # original_rank = original_curr_point_neib_ranking.index(original_dataset[j])
#             original_rank = original_curr_point_neib_ranking_mapping[str(original_dataset[j])]
#             if (reduced_rank <= k) and (original_rank > k):
#                 rank_sum += original_rank - k
#     # print(rank_sum)
#     result = 1 - (2 / (n * k * (2 * n - 3 * k - 1))) * rank_sum
#     return result
#
#
# def get_continuity(reduced_dataset, original_dataset, k):
#     rank_sum = 0
#     n = len(reduced_dataset)
#     for i in range(0, n):
#         curr_point = reduced_dataset[i]
#         curr_point_neib_ranking = sorted(reduced_dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(curr_point)), reverse=False)
#         curr_point_neib_ranking_mapping = dict()
#         for i_2 in range(1, n):
#             curr_point_neib_ranking_mapping[str(curr_point_neib_ranking[i_2])] = i_2
#         original_curr_point = original_dataset[i]
#         original_curr_point_neib_ranking = sorted(original_dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(original_curr_point)), reverse=False)
#         original_curr_point_neib_ranking_mapping = dict()
#         for i_2 in range(1, n):
#             original_curr_point_neib_ranking_mapping[str(original_curr_point_neib_ranking[i_2])] = i_2
#         for j in range(0, n):
#             if i == j:
#                 continue
#             # reduced_rank = get_rank(curr_point, reduced_dataset[j], reduced_dataset)
#             # reduced_rank = curr_point_neib_ranking.index(reduced_dataset[j])
#             reduced_rank = curr_point_neib_ranking_mapping[str(reduced_dataset[j])]
#             # original_rank = get_rank(original_curr_point, original_dataset[j], original_dataset)
#             # original_rank = original_curr_point_neib_ranking.index(original_dataset[j])
#             original_rank = original_curr_point_neib_ranking_mapping[str(original_dataset[j])]
#             if (reduced_rank > k) and (original_rank <= k):
#                 rank_sum += reduced_rank - k
#     # print(rank_sum)
#     result = 1 - (2 / (n * k * (2 * n - 3 * k - 1))) * rank_sum
#     return result


# def get_trustworthiness_and_continuity(reduced_dataset, original_dataset, k):
#     continuity_rank_sum = 0
#     trustworthiness_rank_sum = 0
#     n = len(reduced_dataset)
#     for i in range(0, n):
#         curr_point = reduced_dataset[i]
#         curr_point_neib_ranking = sorted(reduced_dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(curr_point)), reverse=False)
#         curr_point_neib_ranking_mapping = dict()
#         for i_2 in range(1, n):
#             curr_point_neib_ranking_mapping[str(curr_point_neib_ranking[i_2])] = i_2
#         original_curr_point = original_dataset[i]
#         original_curr_point_neib_ranking = sorted(original_dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(original_curr_point)), reverse=False)
#         original_curr_point_neib_ranking_mapping = dict()
#         for i_2 in range(1, n):
#             original_curr_point_neib_ranking_mapping[str(original_curr_point_neib_ranking[i_2])] = i_2
#         for j in range(0, n):
#             if i == j:
#                 continue
#             reduced_rank = curr_point_neib_ranking_mapping[str(reduced_dataset[j])]
#             original_rank = original_curr_point_neib_ranking_mapping[str(original_dataset[j])]
#             if (reduced_rank > k) and (original_rank <= k):
#                 continuity_rank_sum += reduced_rank - k
#             if (reduced_rank <= k) and (original_rank > k):
#                 trustworthiness_rank_sum += original_rank - k
#     # print(rank_sum)
#     trustworthiness = 1 - (2 / (n * k * (2 * n - 3 * k - 1))) * trustworthiness_rank_sum
#     continuity = 1 - (2 / (n * k * (2 * n - 3 * k - 1))) * continuity_rank_sum
#     return trustworthiness, continuity


def get_trustworthiness_and_continuity(reduced_dataset, original_dataset, k):
    continuity_rank_sum = 0
    trustworthiness_rank_sum = 0
    n = len(reduced_dataset)
    reduced_X = np.array(reduced_dataset)
    reduced_nbrs = NearestNeighbors(n_neighbors=n - 1, algorithm='auto').fit(reduced_X)
    reduced_distances, reduced_indices = reduced_nbrs.kneighbors(reduced_X)
    original_X = np.array(original_dataset)
    original_nbrs = NearestNeighbors(n_neighbors=n - 1, algorithm='auto').fit(original_X)
    original_distances, original_indices = original_nbrs.kneighbors(original_X)
    for i in range(0, n):
        # curr_point = reduced_dataset[i]
        # curr_point_neib_ranking = sorted(reduced_dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(curr_point)), reverse=False)
        # curr_point_neib_ranking_mapping = dict()
        # for i_2 in range(1, n):
        #     curr_point_neib_ranking_mapping[str(curr_point_neib_ranking[i_2])] = i_2
        # original_curr_point = original_dataset[i]
        # original_curr_point_neib_ranking = sorted(original_dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(original_curr_point)), reverse=False)
        # original_curr_point_neib_ranking_mapping = dict()
        # for i_2 in range(1, n):
        #     original_curr_point_neib_ranking_mapping[str(original_curr_point_neib_ranking[i_2])] = i_2
        for j in range(0, n):
            if i == j:
                continue
            reduced_rank = np.where(reduced_indices[i] == j)[0]
            original_rank = np.where(original_indices[i] == j)[0]
            if (reduced_rank > k) and (original_rank <= k):
                continuity_rank_sum += reduced_rank - k
            if (reduced_rank <= k) and (original_rank > k):
                trustworthiness_rank_sum += original_rank - k
    # print(rank_sum)
    trustworthiness = 1 - (2 / (n * k * (2 * n - 3 * k - 1))) * trustworthiness_rank_sum
    continuity = 1 - (2 / (n * k * (2 * n - 3 * k - 1))) * continuity_rank_sum
    return trustworthiness, continuity


def get_generalization_error(reduced_dataset, dataset_labels): # leave-one-out
    # reduced_dataset_mapping = dict()
    wrong_predict_count = 0
    X = np.array(reduced_dataset)
    nbrs = NearestNeighbors(n_neighbors=2, algorithm='auto').fit(X)
    distances, indices = nbrs.kneighbors(X)
    n = len(reduced_dataset)
    # for i in range(0, len(reduced_dataset)):
    #     reduced_dataset_mapping[str(reduced_dataset[i])] = i
    for i in range(0, n):
        curr = reduced_dataset[i]
        curr_NN_idx = indices[i][1]
        # curr_NN = get_NN(curr, reduced_dataset)
        # curr_NN_idx = reduced_dataset_mapping[str(curr_NN)]
        curr_predict = dataset_labels[curr_NN_idx]
        ground_truth = dataset_labels[i]
        if curr_predict != ground_truth:
            wrong_predict_count += 1
    return wrong_predict_count / n


def get_artificial_dataset_labels(dataset):
    labels = []
    rows = len(dataset)
    cols = len(dataset[0])
    for i in range(0, rows):
        curr = dataset[i]
        cls = -1
        for j in range(0, cols):
            if round(curr[j]) % 2 == 1:
                cls *= -1
        labels.append(cls)
    return labels


def get_natural_dataset_samples(num_of_samples):
    from loader import MNIST

    import random
    mndata = MNIST('MNIST_dataset')
    images, labels = mndata.load_training()
    selected_img = []
    selected_labels = []
    selected_idxs = random.sample(range(0, len(images)), num_of_samples)
    for i in range(0, len(selected_idxs)):
        # newPoint = [float(j) for j in images[selected_idxs[i]]]
        # selected_img.append(newPoint)
        selected_img.append(images[selected_idxs[i]])
        selected_labels.append(labels[selected_idxs[i]])
    return selected_img, selected_labels



def get_NN(datapoint, dataset):
    ranking = sorted(dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(datapoint)), reverse=False)
    return ranking[1]






# def get_trustworthiness(reduced_dataset, original_dataset, k):
#     rank_sum = 0
#     dists_between_low_dim_datapoints = []
#     n = len(reduced_dataset)
#     for i in range(0, n - 1):
#         for j in range(i + 1, n):
#             point_1 = reduced_dataset[i]
#             point_2 = reduced_dataset[j]
#             dist = np.linalg.norm(np.array(point_1) - np.array(point_2))
#             dists_between_low_dim_datapoints.append(dist)
#     sorted_dists = sorted(dists_between_low_dim_datapoints, key=float)
#     count = 0
#     for i in range(0, n):
#         curr_point = reduced_dataset[i]
#         curr_point_neib_ranking = sorted(reduced_dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(curr_point)), reverse=False)
#         curr_point_neib_ranking_mapping = dict()
#         for i_2 in range(1, n):
#             curr_point_neib_ranking_mapping[str(curr_point_neib_ranking[i_2])] = i_2
#         original_curr_point = original_dataset[i]
#         original_curr_point_neib_ranking = sorted(original_dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(original_curr_point)), reverse=False)
#         original_curr_point_neib_ranking_mapping = dict()
#         for i_2 in range(1, n):
#             original_curr_point_neib_ranking_mapping[str(original_curr_point_neib_ranking[i_2])] = i_2
#         for j in range(0, n):
#             if i == j:
#                 continue
#             # reduced_rank = get_rank(curr_point, reduced_dataset[j], reduced_dataset)
#             # reduced_rank = curr_point_neib_ranking.index(reduced_dataset[j])
#             reduced_rank = curr_point_neib_ranking_mapping[str(reduced_dataset[j])]
#             # original_rank = get_rank(original_curr_point, original_dataset[j], original_dataset)
#             # original_rank = original_curr_point_neib_ranking.index(original_dataset[j])
#             original_rank = original_curr_point_neib_ranking_mapping[str(original_dataset[j])]
#             if (reduced_rank <= k) and (original_rank > k):
#                 curr_dist = np.linalg.norm(np.array(curr_point) - np.array(reduced_dataset[j]))
#                 print(reduced_rank)
#                 count += 1
#                 rank_sum += sorted_dists.index(curr_dist) + 1 - k
#     print(count)
#     result = 1 - (2 / (n * k * (2 * n - 3 * k - 1))) * rank_sum
#     return result




# def get_rank(datapoint_1, datapoint_2, dataset):    # what if two points have exactly the same coordinate?
#     ranking = sorted(dataset, key=lambda l: np.linalg.norm(np.array(l) - np.array(datapoint_1)), reverse=False)
#     ranking.remove(datapoint_1)
#     for x in range(0, len(ranking)):
#         if ranking[x] == datapoint_2:
#             return x + 1
#     return -1

