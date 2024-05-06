from typing import Literal, Callable
import numpy as np
from collections import Counter

class Node:
    def __init__(self,
        predicted_value: float | int | None = None,
        feature: int | None = None,
        threshold: float | int | None = None,
        left_child = None,
        right_child = None
    ):
        self.predicted_value = predicted_value
        self.feature = feature
        self.threshold = threshold
        self.left_child = left_child
        self.right_child = right_child

def mean_squared_error(column: np.ndarray):
    return np.mean((column - np.mean(column))**2 )

def mean_absolute_error(column: np.ndarray):
    return np.sum(np.absolute(column - np.mean(column))) / column.shape[0]

def entropy(column: np.ndarray):
    probabilities = np.array(list(Counter(column).values())) / len(column)
    return -np.sum(probabilities * np.log2(probabilities))

def gini(column: np.ndarray):
    column = np.sort(column)
    n = column.shape[0]
    index = np.arange(1, n + 1)
    return ((np.sum((2 * index - n  - 1) * column)) / (n * np.sum(column)))

def null(x) -> bool:
    return x.shape[0] == 0 if type(x) is np.ndarray else not bool(x)

class CART:
    """Classification and regression tree"""
    CRITERIONS = {
        'squared_error': mean_squared_error ,
        'absolute_error': mean_absolute_error,
        'entropy': entropy,
        'gini': gini,
    }

    @staticmethod
    def __initialization(func):
        def init_wrapper(*args, **kwargs):
            func(*args, **kwargs)
            self: CART = args[0]
            if self.criterion not in CART.CRITERIONS:
                raise ValueError(f'Criterion {self.criterion} not exists')
            elif self.criterion in ['squared_error', 'absolute_error']:
                self.list = lambda Y: Node(np.mean(Y))
            else: # classification
                self.list = lambda Y: Node(Counter(Y).most_common(1)[0][0])
            self.criterion = CART.CRITERIONS[self.criterion]
        return init_wrapper

    @__initialization
    def __init__(
        self,
        criterion: Literal['squared_error', 'absolute_error', 'entropy', 'gini'],
        max_depth: int | None = None,
        min_samples_split: int = 2
    ) -> None:
        self.max_depth = max_depth
        self.criterion = criterion
        self.min_samples_split = min_samples_split
        self.list: Callable[[np.ndarray], float | int] | None = None

    def __split_dataset(
        self, X: np.ndarray, y: np.ndarray, feature: int, threshold: float
    ):
        left_indexes = np.where(X[:, feature] <= threshold)[0]
        right_indexes = np.where(X[:, feature] > threshold)[0]
        return X[left_indexes], y[left_indexes], X[right_indexes], y[right_indexes]

    def __find_best_split(self, X: np.ndarray, y: np.ndarray):
        best_feature, best_threshold, best_criterion_score = None, None, np.inf
        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                _, y_left, _, y_right = self.__split_dataset(X, y, feature, threshold)
                if not (null(y_left) or null(y_right)):
                    criterion_score = (len(y_left) * self.criterion(y_left) +
                        len(y_right) * self.criterion(y_right)) / len(y)
                    if criterion_score < best_criterion_score:
                        best_feature, best_threshold, best_criterion_score = (
                            feature, threshold, criterion_score)
        return best_feature, best_threshold

    def __build_tree(self, X: np.ndarray, y: np.ndarray, depth: int = 0):
        if depth == self.max_depth or len(X) <= self.min_samples_split:
            return self.list(y)
        feature, threshold = self.__find_best_split(X, y)
        if not threshold:
            return self.list(y)
        x_left, y_left, x_right, y_right = self.__split_dataset(X, y, feature, threshold)
        left_child = self.__build_tree(x_left, y_left, depth + 1)
        right_child = self.__build_tree(x_right, y_right, depth + 1)
        return Node(feature=feature,
                    threshold=threshold,
                    left_child=left_child,
                    right_child=right_child)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.root = self.__build_tree(np.array(X), np.array(y))
        return self

    def __predict_single(self, X: np.ndarray, node: Node):
        while isinstance(node.feature, int):
            node = node.left_child if X[node.feature] <= node.threshold else node.right_child
        return node.predicted_value

    def predict(self, X: np.ndarray):
        return [self.__predict_single(x, self.root) for x in np.array(X)]
