# 🧠🤖 Neural Networks: MLP vs. MCP  

📄 **Project Report**: [Read the Full Report 📑](https://github.com/hishamikoo/Neural-Networks-MLP-vs-MCP/blob/main/MLP%20vs%20MCP%20-%20Report.pdf)  

## 📌 Overview  
This research explores the performance of neural networks—**Multi-Layer Perceptron (MLP) 🏗️** vs. **Multi-Class Perceptron (MCP) 🔀**compared to traditional classifiers like **K-Nearest Neighbors (KNN) 📍** and **Naïve Bayes 🎲**.  

## 🔍 Key Insights  
📉 **MLP struggles with deeper layers**: Despite using a sophisticated architecture, MLP achieved just **~45% accuracy**, which is **lower** than KNN and Naïve Bayes. However, with **only 1 hidden layer**, MLP performed significantly better.  

📊 **Why did this happen?**  
- 🚧 **Model complexity** led to overfitting and poor generalization  
- 🔍 **KNN leveraged PCA & cross-validation** for **better feature representation**  
- 🎯 **Naïve Bayes remained stable** without the need for heavy tuning  

## ⚖️ Performance Comparison  
| Model | Strengths 💪 | Weaknesses ⚠️ |
|--------|------------|--------------|
| **MLP (Multi-Layer Perceptron) 🏗️** | Can model complex relationships | Overfitting, needs hyperparameter tuning |
| **MCP (Multi-Class Perceptron) 🔀** | Simpler and faster than MLP | Struggles with non-linearly separable data |
| **KNN (K-Nearest Neighbors) 📍** | Works well with PCA & tuning | Sensitive to noisy data & computationally expensive |
| **Naïve Bayes 🎲** | Fast, interpretable, and works well with categorical data | Assumes feature independence, limiting real-world performance |

### 🏆 Best Performing Model: **KNN**  
- 📈 **Optimal accuracy** with **K values between 6-8**  
- 🔬 **Best training-testing split**: **60:40**  

## 🚀 Improving Neural Network Performance  
To enhance MLP’s accuracy, we suggest:  
✅ **Hyperparameter tuning** (e.g., grid search, learning rate adjustments)  
✅ **Regularization techniques** (e.g., dropout, L2 regularization)  
✅ **Feature engineering** (optimizing input features for better representation)  
✅ **Alternative architectures** (e.g., CNNs or transformer-based models for more complex tasks)  

## 🎯 Conclusion  
This study emphasizes the **importance of model selection** for different datasets. While **KNN and Naïve Bayes** performed best for the **Palmer Penguins dataset**, **MLP has great potential** for more **complex** applications **if optimized correctly**.  

🔬 **Key Takeaway:** **Simple models can often outperform deep learning when data and hyperparameters are not optimized effectively.**  
