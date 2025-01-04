# Neural-Networks-MLP-vs-MCP
This research explores the performance of neural networks (MLP vs. MCP) compared to traditional classifiers (KNN and Naïve Bayes).

The analysis of the Palmer Penguins dataset using neural networks has highlighted some critical
limitations alongside its potential. Despite employing a sophisticated model with multiple
hidden layers, the neural network achieved just over 45% accuracy, which is significantly lower
than the performance of K-Nearest Neighbors (KNN) and Naïve Bayes classifiers. On the
contrary, it performs really well with just 1 hidden layer. These limitations may stem from the
model's complexity. In contrast, KNN benefited from cross-validation and principal component
analysis (PCA), effectively capturing the spatial relationships between features, while Naïve
Bayes provided stable results without extensive tuning.

When comparing the effectiveness of these approaches, KNN demonstrated optimal
performance with a training-testing split of 60:40 and tuning K values between 6 and 8,
maximizing accuracy and robustness. Naïve Bayes, known for its speed and interpretability,
excelled in scenarios with categorical data, providing consistent results even without significant
preprocessing. The neural network's struggles with accuracy reflect the challenges of overfitting
and the need for careful architecture design and hyperparameter tuning, as its complexity often
requires more extensive data and fine-tuning than simpler models.

To improve the neural network's performance, hyperparameter optimization techniques like
grid search could enhance model tuning, while regularization methods can help prevent
overfitting. Additionally, refining input features through feature engineering and considering
alternative model architectures may yield better results. Overall, this comparison underscores
the importance of selecting the appropriate model for the dataset and classification task,
suggesting that while KNN and Naïve Bayes are effective for the penguin dataset, neural
networks hold potential for more complex applications if optimized correctly.
