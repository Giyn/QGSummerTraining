[TOC]

# 贝叶斯分类器

## 贝叶斯决策论

​		贝叶斯决策论 (Bayesian decision theory) 是概率框架下实施决策的基本方法。对分类任务来说，在所有相关概率都已知的理想情形下，贝叶斯决策论考虑如何基于这些概率和误判损失来选择最优的类别标记。下面以多分类任务为例来解释其基本原理。

​		假设有 $N$ 种可能的类别标记，即 $γ=\{c_1,c_2,...,c_n\}$，$\lambda_{ij}$ 是将一个真实标记为 $c_j$ 的样本误分类为 $c_i$ 所产生的损失。基于后验概率 $P(c_i\mid x)$ 可获得将样本 $x$ 分类为 $c_i$ 所产生的期望损失(expected loss)，即在样本 $x$ 上的“条件风险”(conditional risk)
$$
R(c_i\mid x)=\sum^N_{j=1}\lambda_{ij}P(c_j\mid x)\,\,.\tag{1}
$$

>决策论中将“期望损失”称为“风险”(risk)。

我们的任务是寻找一个判定准则 $h:\chi \rightarrow γ$ 以最小化总体风险
$$
R(h)=\mathbb E_x\left[R(h(x)\mid x)\right]\,\,.\tag{2}
$$
显然，对每个样本 $x$，若 $h$ 能最小化条件风险 $R(h(x)\mid x)$，则总体风险 $R(h)$ 也将被最小化。这就产生了贝叶斯判定准则 (Bayes decision rule)：为最小化总体风险，只需在每个样本上选择那个能使条件风险 $R(c\mid x)$ 最小的类别标记，即
$$
h^*(x)=\mathop{\arg\min}_{c∈γ}R(c\mid x)\,\,,\tag{3}
$$
此时，$h^*$ 称为贝叶斯最优分类器 (Bayes optimal classifer)，与之对应的总体风险 $R(h^*)$ 称为贝叶斯风险(Bayes risk)。$1-R(h^*)$ 反映了分类器所能达到的最好性能，即通过机器学习所能产生的模型精度的理论上限。
		具体来说，若目标是最小化分类错误率，则误判损失 $\lambda{ij}$ 可写为
$$
\lambda_{ij}=
\begin{cases}
0,\quad{if\,\,\,i=j\,\,;}\\
1,\quad{otherwise}\,,
\end{cases}
\tag{4}
$$
此时条件风险
$$
R(c\mid x)=1-P(c\mid x)\,\,,\tag{5}
$$
于是，最小化分类错误率的贝叶斯最优分类器为
$$
h^*(x)=\mathop{\arg\max}_{c∈γ}P(c\mid x)\,\,,\tag{6}
$$
即对每个样本 $x$，选择能使后验概率 $P(c\mid x)$ 最大的类别标记。

​		不难看出，欲使用贝叶斯判定准则来最小化决策风险，首先要获得后验概率 $P(c\mid x)$。然而，在现实任务中这通常难以直接获得。从这个角度来看，机器学习所要实现的是基于有限的训练样本集尽可能准确地估计出后验概率 $P(c\mid x)$。

​		大体来说，主要有两种策略：

- 给定 $x$，可通过直接建模 $P(c\mid x)$ 来预测 $c$，这样得到的是“判别式模型”(discriminative models)；
- 先对联合概率分布 $P(x,c)$ 建模，然后再由此获得 $P(c\mid x)$，这样得到的是“生成式模型”(generative models)。

​		显然，前面介绍的决策树、$BP$ 神经网络、支持向量机等，都可归入判别式模型的范畴。对生成式模型来说，必然考虑
$$
P(c\mid x)=\frac{P(x,c)}{P(x)}\,\,.\tag{7}
$$
​		基于贝叶斯定理，$P(c\mid x)$ 可写为
$$
P(c\mid x)=\frac{P(c)P(x\mid c)}{P(x)}\,\,,\tag{8}
$$
其中，$P(c)$ 是类“先验”(prior)概率；$P(x\mid c)$ 是样本 $x$ 相对于类标记 $c$ 的类条件概率(class conditional probability)，或称为“似然”(ikelihood)；$P(x)$ 是用于归一化的“证据”(evidence)因子。对给定样本 $x$，证据因子 $P(x)$ 与类标记无关，因此估计 $P(c\mid x)$ 的问题就转化为如何基于训练数据 $D$ 来估计先验 $P(c)$ 和似然 $P(x\mid c)$。

​		类先验概率 $P(c)$ 表达了样本空间中各类样本所占的比例，根据大数定律，当训练集包含充足的独立同分布样本时，$P(c)$ 可通过各类样本出现的频率来进行估计。

​		对类条件概率 $P(x\mid c)$ 来说，由于它涉及关于 $x$ 所有属性的联合概率，直接根据样本出现的频率来估计将会遇到严重的困难。例如，假设样本的 $d$ 个属性都是二值的，则样本空间将有 $2^d$ 种可能的取值，在现实应用中，这个值往往远大于训练样本数 $m$，也就是说，很多样本取值在训练集中根本没有出现，直接使用频率来估计 $P(x\mid c)$ 显然不可行，因为“未被观测到”与“出现概率为零”通常是不同的。



## 极大似然估计

​		估计类条件概率的一种常用策略是先假定其具有某种确定的概率分布形式，再基于训练样本对概率分布的参数进行估计。具体地，记关于类别 $c$ 的类条件概率为 $P(x\mid c)$，假设 $P(x\mid c)$ 具有确定的形式并且被参数向量 $θ_c$ 唯一确定，则我们的任务就是利用训练集 $D$ 估计参数 $θ_c$。为明确起见，我们将 $P(x\mid c)$ 记为 $P(x\mid \theta_c)$。

​		事实上，概率模型的训练过程就是参数估计(parameter estimation)过程。

​		对于参数估计，统计学界的两个学派分别提供了不同的解决方案：

- 频率主义学派(Frequentist)认为参数虽然未知，但却是客观存在的固定值，因此，可通过优化似然函数等准则来确定参数值；
- 贝叶斯学派(Bayesian)则认为参数是未观察到的随机变量，其本身也可有分布，因此，可假定参数服从一个先验分布，然后基于观测到的数据来计算参数的后验分布。

​		此处介绍源自频率主义学派的极大似然估计(Maximum Likelihood Estimation，简称MLE)，这是根据数据采样来估计概率分布参数的经典方法。

​		令 $D_c$ 表示训练集 $D$ 中第 $c$ 类样本组成的集合，假设这些样本是独立同分布的，则参数 $θ_c$ 对于数据集 $D_c$ 的似然是
$$
P(D_c\mid \theta_c)=\prod_{x∈D_c}P(x\mid \theta_c)\,\,.\tag{9}
$$
对 $θ_c$ 进行极大似然估计，就是去寻找能最大化似然 $P(D_c\mid \theta_c)$ 的参数值 $\hat{θ}_c$。直观上看，极大似然估计是试图在 $θ_c$ 所有可能的取值中，找到一个能使数据出现的“可能性”最大的值。
		式 (9) 中的连乘操作易造成下溢，通常使用对数似然(log-likelihood)
$$
\begin{align}
LL(\theta_c)&=log\,\,P(D_c\mid\theta_c)\\
&=\sum_{x∈D_c}log\,\,P(x\mid\theta_c)\,\,,\tag{10}
\end{align}
$$
此时参数 $θ_c$ 的极大似然估计白 $\hat{θ}_c$ 为
$$
\hat{θ}_c=\mathop{\arg\max}_{\theta_c}LL(\theta_c)\,\,.\tag{11}
$$
​		例如，在连续属性情形下，假设概率密度函数 $p(x\mid c)\sim N(μ_c,\sigma^2_c)$，则参数μc和σ2的极大似然估计为
$$
\hat{\mu}_c=\frac{1}{|D_c|}\sum_{x∈D_c}x\,\,,\tag{12}
$$

$$
\hat{\sigma}_c^2=\frac{1}{|D_c|}\sum_{x∈D_c}(x-\hat{\mu}_c)(x-\hat{\mu}_c)^T\,\,.\tag{13}
$$

也就是说，通过极大似然法得到的正态分布均值就是样本均值，方差就是 $(x-\hat{\mu}_c)(x-\hat{\mu}_c)^T$ 的均值，这显然是一个符合直觉的结果。在离散属性情形下，也可通过类似的方式估计类条件概率。
		需注意的是，这种参数化的方法虽能使类条件概率估计变得相对简单，但估计结果的准确性严重依赖于所假设的概率分布形式是否符合潜在的真实数据分布。在现实应用中，欲做出能较好地接近潜在真实分布的假设，往往需在一定程度上利用关于应用任务本身的经验知识，否则若仅凭“猜测”来假设概率分布形式，很可能产生误导性的结果。



## 朴素贝叶斯分类器

​		不难发现，基于贝叶斯公式 (8) 来估计后验概率 $P(c\mid x)$ 的主要困难在于：类条件概率 $P(x\mid c)$ 是所有属性上的联合概率，难以从有限的训练样本直接估计而得。

> 基于有限训练样本直接估计联合概率，在计算上将会遭遇组合爆炸问题，在数据上将会遭遇样本稀疏问题；属性数越多，问题越严重。

​		为避开这个障碍，朴素贝叶斯分类器 (naive Bayes classifer) 采用了“属性条件独立性假设” (attribute conditional independence assimption)：对已知类别，假设所有属性相互独立。换言之，假设每个属性独立地对分类结果发生影响。



### $NavieBayes$ 算法流程：

1. 导入数据集，确定特征属性；

2. 对每个类别计算 $P(y_i)$；

3. 对每个特征属性计算所有划分的条件概率；

4. 对每个类别计算 $P(x\mid y_i)P(y_i)$；

5. 以 $$P(x\mid y_i)P(y_i)$$ 最大项作为 $x$ 所属类别；



​		基于属性条件独立性假设，式 (8) 可重写为
$$
P(c\mid x)=\frac{P(c)P(x\mid c)}{P(x)}=\frac{P(c)}{P(x)}\prod^d_{i=1}P(x_i\mid c)\,\,,\tag{14}
$$
其中 $d$ 为属性数目，$x_i$ 为 $x$ 在第 $i$ 个属性上的取值。
		由于对所有类别来说 $P(x)$ 相同，因此基于式 (6) 的贝叶斯判定准则有
$$
h_{nb}(x)=\mathop{\arg\max}_{c∈\gamma}\,\,P(c)\prod^d_{i=1}P(x_i\mid c)\,\,,\tag{15}
$$
这就是朴素贝叶斯分类器的表达式.
		显然，朴素贝叶斯分类器的训练过程就是基于训练集 $D$ 来估计类先验概率 $P(c)$，并为每个属性估计条件概率 $P(x_i\mid c)$。
		令 $D_c$ 表示训练集 $D$ 中第 $c$ 类样本组成的集合，若有充足的独立同分布样本，则可容易地估计出类先验概率
$$
P(c)=\frac{|D_c|}{|D|}\,\,.\tag{16}
$$
对离散属性而言，令 $D_{c_,x_i}$ 表示 $D_c$ 中在第 $i$ 个属性上取值为 $x_i$ 的样本组成的集合，则条件概率 $P(x_i\mid c)$ 可估计为
$$
P(x_i\mid c)=\frac{|D_{c_,x_i}|}{|D_c|}\,\,.\tag{17}
$$
对连续属性可考虑概率密度函数，假定 $p(x_i\mid c)\sim N(μ_{c_,i},\sigma^2_{c,i})$，其中 $μ_{c_,i}$ 和 $\sigma^2_{c,i}$ 分别是第 $c$ 类样本在第 $i$ 个属性上取值的均值和方差，则有
$$
p(x_i\mid c)=\frac{1}{\sqrt{2\pi}\sigma_{c,i}}exp\left(-\frac{(x_i-\mu_{c,i})^2}{2\sigma^2_{c,i}}\right)\,\,.\tag{18}
$$

> 实践中常通过取对数的方式来将“连乘”转化为“连加”以避免数值下溢。

​		为了避免其他属性携带的信息被训练集中未出现的属性值“抹去”，在估计概率值时通常要进行“平滑”(smoothing)，常用“拉普拉斯修正”(Laplacian correction)。具体来说，令 $N$ 表示训练集 $D$ 中可能的类别数，$N_i$ 表示第 $i$ 个属性可能的取值数，则式 (16) 和 (17) 分别修正为
$$
\hat{P}(c)=\frac{|D_c|+1}{|D|+N}\,\,,\tag{19}
$$

$$
\hat{P}(x_i\mid c)=\frac{|D_{c,x_i}|+1}{|D_c|+N_i}\,\,.\tag{20}
$$

显然，拉普拉斯修正避免了因训练集样本不充分而导致概率估值为零的问题，并且在训练集变大时，修正过程所引入的先验(prior)的影响也会逐渐变得可忽略，使得估值渐趋向于实际概率值。

>拉普拉斯修正实质上假设了属性值与类别均匀分布，这是在朴素贝叶斯学习过程中额外引入的关于数据的先验。

​		在现实任务中朴素贝叶斯分类器有多种使用方式。例如，若任务对预测速度要求较高，则对给定训练集，可将朴素贝叶斯分类器涉及的所有概率估值事先计算好存储起来，这样在进行预测时只需“查表”即可进行判别；若任务数据更替频繁，则可采用“懒惰学习” (lazy learning) 方式，先不进行任何训练，待收到预测请求时再根据当前数据集进行概率估值；若数据不断增加，则可在现有估值基础上，仅对新增样本的属性值所涉及的概率估值进行计数修正即可实现增量学习。



### 朴素贝叶斯算法优缺点：

#### 优点：

- 朴素贝叶斯模型发源于古典数学理论，有着坚实的数学基础，以及稳定的分类效率。
- 对大数量训练和查询时具有较高的速度。即使使用超大规模的训练集，针对每个项目通常也只会有相对较少的特征数，并且对项目的训练和分类也仅仅是特征概率的数学运算而已；
- 对小规模的数据表现很好，能个处理多分类任务，适合增量式训练（即可以实时的对新增的样本进行训练）；
- 对缺失数据不太敏感，算法也比较简单，常用于文本分类；
- 朴素贝叶斯对结果解释容易理解。

#### 缺点：

- 需要计算先验概率；
- 分类决策存在错误率；
- 对输入数据的表达形式很敏感；
- 由于**使用了样本属性独立性的假设，所以如果样本属性有关联时其效果不好。**



## 半朴素贝叶斯分类器

​		为了降低贝叶斯公式 (8) 中估计后验概率 $P(c\mid x)$ 的困难，朴素贝叶斯分类器采用了属性条件独立性假设，但在现实任务中这个假设往往很难成立。于是，人们尝试对属性条件独立性假设进行一定程度的放松，由此产生了一类称为“半朴素贝叶斯分类器”(semi-naive Bayes classfers)的学习方法。
​		半朴素贝叶斯分类器的基本想法是适当考虑一部分属性间的相互依赖信息，从而既不需进行完全联合概率计算，又不至于彻底忽略了比较强的属性依赖关系、“独依赖估计”(One-Dependent Estimator，简称ODE)是半朴素贝叶斯分类器最常用的一种策略。顾名思义，所谓“独依赖”就是假设每个属性在类别之外最多仅依赖于一个其他属性，即
$$
P(c\mid x)\propto P(c)\prod^d_{i=1}P(x_i\mid c,pa_i)\,\,,\tag{21}
$$
其中 $pa_i$ 为属性 $x_i$ 所依赖的属性，称为 $x_i$ 的父属性。此时，对每个属性 $x_i$，若父属性 $pa_i$ 已知，则可采用类似式 (20) 的办法来估计概率值 $P(x_i\mid c,pa_i)$。于是，问题的关键就转化为如何确定每个属性的父属性，不同的做法产生不同的独依赖分类器。

​		最直接的做法是假设所有属性都依赖于同一个属性，称为“超父”(super-parent)，然后通过交叉验证等模型选择方法来确定超父属性，由此形成了 SPODE (Super-Parent ODE) 方法。例如，在下图(b)中，$x_1$ 是超父属性。

![朴素贝叶斯与两种半朴素贝叶斯分类器所考虑的属性依赖关系.png](https://github.com/Giyn/QG2020SummerTraining/blob/master/Pictures/NaiveBayes/%E6%9C%B4%E7%B4%A0%E8%B4%9D%E5%8F%B6%E6%96%AF%E4%B8%8E%E4%B8%A4%E7%A7%8D%E5%8D%8A%E6%9C%B4%E7%B4%A0%E8%B4%9D%E5%8F%B6%E6%96%AF%E5%88%86%E7%B1%BB%E5%99%A8%E6%89%80%E8%80%83%E8%99%91%E7%9A%84%E5%B1%9E%E6%80%A7%E4%BE%9D%E8%B5%96%E5%85%B3%E7%B3%BB.png?raw=true)

​		TAN​ (Tree Augmented naive Bayes) 则是在最大带权生成树 (maximum weighted spanning tree) 算法的基础上，通过以下步骤将属性间依赖关系约简为如上图 (c) 所示的树形结构：

1. 计算任意两个属性之间的条件互信息(conditional mutual information)。

$$
I(x_i,x_j\mid y)=\sum_{x_i,x_j;\,c∈\gamma}P(x_i,x_j\mid c)\,log\frac{P(x_i,x_j\mid c)}{P(x_i\mid c)P(x_j\mid c)}\,\,;\tag{22}
$$

2. 以属性为结点构建完全图，任意两个结点之间边的权重设为 $I(x_i,x_j\mid y)$。

3. 构建此完全图的最大带权生成树，挑选根变量，将边置为有向；

4. 加入类别结点 $y$，增加从 $y$ 到每个属性的有向边。

​		容易看出，条件互信息 $I(x_i,x_j\mid y)$ 刻画了属性 $x_i$ 和 $x_j$ 在已知类别情况下的相关性，因此，通过最大生成树算法，TAN 实际上仅保留了强相关属性之间的依赖性。
​		AODE (Averaged One-Dependent Estimator) 是一种基于集成学习机制、更为强大的独依赖分类器。与 SPODE 通过模型选择确定超父属性不同，AODE尝试将每个属性作为超父来构建 SPODE，然后将那些具有足够训练数据支撑的 SPODE 集成起来作为最终结果，即
$$
P(c\mid x)\propto \sum^d_{\substack{i=1\\|D_{x_i}|\geq m'}_d}
P(c,x_i)\prod^d_{j=1}P(x_j\mid c,x_i)\,\,,\tag{23}
$$

> $m'$ 默认设为 30。

其中 $D_{x_i}$ 是在第 $i$ 个属性上取值为 $x_i$ 的样本的集合，$m'$ 为阈值常数。显然，AODE 需估计 $P(c,x_i)$ 和 $P(x_j\mid c,x_i)$。类似式 (20)，有
$$
\hat{P}(c,x_i)=\frac{|D_{c,x_i}|+1}{|D|+N_i}\,\,,\tag{24}
$$

$$
\hat{P}(x_j\mid c,x_i)=\frac{|D_{c,x_i,x_j}|+1}{|D_{c,x_i}|+N_j}\,\,,\tag{25}
$$

其中 $N_i$ 是第 $i$ 个属性可能的取值数，$D_{c,x_i}$ 是类别为 $c$ 且在第 $i$ 个属性上取值为 $x_i$ 的样本集合，$D_{c,x_i,x_j}$ 是类别为 $c$ 且在第 $i$ 和第 $j$ 个属性上取值分别为 $x_i$ 和 $x_j$ 的样本集合。

​		不难看出，与朴素贝叶斯分类器类似，AODE 的训练过程也是“计数”，即在训练数据集上对符合条件的样本进行计数的过程。与朴素贝叶斯分类器相似，AODE 无需模型选择，既能通过预计算节省预测时间，也能采取懒惰学习方式在预测时再进行计数，并且易于实现增量学习。

​		既然将属性条件独立性假设放松为独依赖假设可能获得泛化性能的提升，那么，能否通过考虑属性间的高阶依赖来进一步提升泛化性能呢？也就是说，将式 (23) 中的属性 $pa_i$ 替换为包含 $k$ 个属性的集合 $pa_i$，从而将 ODE 拓展为 kDE。需注意的是，随着 $k$ 的增加，准确估计概率 $P(x_i\mid y,pa_i)$ 所需的训练样本数量将以指数级增加。因此，若训练数据非常充分，泛化性能有可能提升；但在有限样本条件下，则又陷入估计高阶联合概率的泥沼。

>“高阶依赖”即对多个属性依赖。



## 贝叶斯网

​		贝叶斯网 (Bayesian network) 亦称“信念网”(belief network)，它借助有向无环图 (Directed Acyclic Graph，简称DAG) 来刻画属性之间的依赖关系，并使用条件概率表 (Conditional Probability Table，简称CPT) 来描述属性的联合概率分布。
​		具体来说，一个贝叶斯网 $B$ 由结构 $G$ 和参数 $\Theta$ 两部分构成，即 $B=\langle G,\Theta\rangle$。网络结构 $G$ 是一个有向无环图，其每个结点对应于一个属性，若两个属性有直接依赖关系，则它们由一条边连接起来；参数 $\Theta$ 定量描述这种依赖关系，假设属性 $x_i$ 在 $G$ 中的父结点集为 $π_i$，则 $\Theta$ 包含了每个属性的条件概率表 $\theta_{x_i|\pi_i}=P_B(x_i\mid \pi_i)$。



### 结构

​		贝叶斯网结构有效地表达了属性间的条件独立性。给定父结点集，贝叶斯网假设每个属性与它的非后裔属性独立，于是 $B=\langle G,\Theta\rangle$ 将属性 $x_1,x_2,...,x_d$ 的联合概率分布定义为
$$
P_B(x_1,x_2,...,x_d)=\prod^d_{i=1}P_B(x_i\mid\pi_i)=\prod^d_{i=1}\theta_{x_i\mid\pi_i}\,\,.\tag{26}
$$
​		下图显示出贝叶斯网中三个变量之间的典型依赖关系，其中前两种在式 (26) 中已有所体现。

![贝叶斯网中三个变量之间的典型依赖关系.png](https://github.com/Giyn/QG2020SummerTraining/blob/master/Pictures/NaiveBayes/%E8%B4%9D%E5%8F%B6%E6%96%AF%E7%BD%91%E4%B8%AD%E4%B8%89%E4%B8%AA%E5%8F%98%E9%87%8F%E4%B9%8B%E9%97%B4%E7%9A%84%E5%85%B8%E5%9E%8B%E4%BE%9D%E8%B5%96%E5%85%B3%E7%B3%BB.png?raw=true)

​		在“同父” (common parent) 结构中，给定父结点 $x_1$ 的取值，则 $x_3$ 与 $x_4$ 条件独立。在“顺序”结构中，给定 $x$ 的值，则 $y$ 与 $z$ 条件独立。V 型结构 (V-structure) 亦称“冲撞”结构，给定子结点 $x_4$ 的取值，$x_1$ 与 $x_2$ 必不独立；奇妙的是，若 $x_4$ 的取值完全未知，则 V 型结构下 $x_1$ 与 $x_2$ 却是相互独立的。我们做一个简单的验证：
$$
\begin{align}
P(x_1,x_2)&=\sum_{x_4}
P(x_1,x_2,x_4)\\
&=\sum_{x_4}P(x_4\mid x_1,x_2)P(x_1)P(x_2)\\
&=P(x_1)P(x_2)\,\,.\tag{27}
\end{align}
$$
这样的独立性称为“边际独立性” (marginal independence)，记为 $x1\perp\!\!\!\perp x2$。

>对变量做积分或求和亦称“边际化”(marginalization)。

​		事实上，一个变量取值的确定与否，能对另两个变量间的独立性发生影响，这个现象并非 V 型结构所特有。例如在同父结构中，条件独立性 $x3\,\,\bot\,\,x4\mid x1$ 成立，但若 $x_1$ 的取值未知，则 $x_3$ 和 $x_4$ 就不独立，即 $x3\perp\!\!\!\perp x4$ 不成立；在顺序结构中，$y\,\,\bot\,\,z\mid x$，但 $y\perp\!\!\!\perp z$ 不成立。

​		为了分析有向图中变量间的条件独立性，可使用“有向分离”(D-separation)。我们先把有向图转变为一个无向图：

- 找出有向图中的所有 V 型结构，在 V 型结构的两个父结点之间加上一条无向边；
- 将所有有向边改为无向边。



由此产生的无向图称为“道德图” (moral graph)，令父结点相连的过程称为“道德化” (moralization) 。
		基于道德图能直观、迅速地找到变量间的条件独立性。假定道德图中有变量 $x$，$y$ 和变量集合 $z=\{z_i\}$，若变量 $x$ 和 $y$ 能在图上被 $z$ 分开，即从道德图中将变量集合 $z$ 去除后, $x$ 和 $y$ 分属两个连通分支，则称变量 $x$ 和 $y$ 被 $z$ 有向分离，$x\,\,\bot\,\,y\mid z$ 成立。



### 学习

​		若网络结构已知，即属性间的依赖关系已知，则贝叶斯网的学习过程相对简单，只需通过对训练样本“计数”，估计出每个结点的条件概率表即可。但在现实应用中我们往往并不知晓网络结构，于是，贝叶斯网学习的首要任务就是根据训练数据集来找出结构最“恰当”的贝叶斯网，“评分搜索” 是求解这一问题的常用办法。具体来说，我们先定义一个评分函数(score function)，以此来评估贝叶斯网与训练数据的契合程度，然后基于这个评分函数来寻找结构最优的贝叶斯网。显然，评分函数引入了关于我们希望获得什么样的贝叶斯网的归纳偏好。

​		常用评分函数通常基于信息论准则，此类准则将学习问题看作一个数据压缩任务，学习的目标是找到一个能以最短编码长度描述训练数据的模型，此时编码的长度包括了描述模型自身所需的字节长度和使用该模型描述数据所需的字节长度。对贝叶斯网学习而言，模型就是一个贝叶斯网，同时，每个贝叶斯网描述了一个在训练数据上的概率分布，自有一套编码机制能使那些经常出现的样本有更短的编码。于是，我们应选择那个综合编码长度 (包括描述网络和编码数据) 最短的贝叶斯网，这就是“最小描述长度” (Minimal DescriptionLength，简称MDL) 准则。

​		给定训练集 $D=\{x_1,x_2,...,x_m\}$，贝叶斯网 $B=\langle G,\Theta\rangle$ 在 $D$ 上的评分函数可写为
$$
s(B\mid D)=f(\theta)|B|-LL(B\mid D)\,\,,\tag{28}
$$

>此处把类别也看作一个属性，即 $x_i$ 是一个包括示例和类别的向量。

其中，$|B|$ 是贝叶斯网的参数个数；$f(\theta)$ 表示描述每个参数 $θ$ 所需的字节数；而
$$
LL(B\mid D)=\sum^m_{i=1}log\,P_B(x_i)\tag{29}
$$
是贝叶斯网 $B$ 的对数似然。显然，式 (28) 的第一项是计算编码贝叶斯网 $B$ 所需的字节数，第二项是计算 $B$ 所对应的概率分布 $P_B$ 需多少字节来描述 $D$。于是，学习任务就转化为一个优化任务，即寻找一个贝叶斯网 $B$ 使评分函数 $s(B\mid D)$ 最小。

​		若 $f(\theta)=1$，即每个参数用 $1$ 字节描述，则得到 AIC (Akaike Information Criterion) 评分函数
$$
AIC(B\mid D)=|B|-LL(B\mid D)\,\,.\tag{30}
$$
​		若 $f(\theta)=\frac{1}{2}log\,m$，即每个参数用 $\frac{1}{2}log\,m$ 字节描述，则得到 BIC (Bayesian Information Criterion) 评分函数
$$
BIC(B\mid D)=\frac{log\,m}{2}|B|-LL(B\mid D)\,\,.\tag{31}
$$
​		显然，若 $f(\theta) = 0$，即不计算对网络进行编码的长度，则评分函数退化为负对数似然，相应地，学习任务退化为极大似然估计。	
​		不难发现，若贝叶斯网 $B=\langle G,\Theta\rangle$ 的网络结构 $G$ 固定，则评分函数 $s(B\mid D)$ 的第一项为常数。此时，最小化 $s(B\mid D)$ 等价于对参数 $\Theta$ 的极大似然估计。由式 (29) 和 (26) 可知，参数 $\theta_{x_i|\pi_i}$ 能直接在训练数据 $D$ 上通过经验估计获得，即
$$
\theta_{x_i|\pi_i}=\hat{P}_D(x_i|\pi_i)\,\,,\tag{32}
$$

>即事件在训练数据上出现的频率。

其中 $\hat{P}_D(·)$ 是 $D$ 上的经验分布。因此，为了最小化评分函数 $s(B\mid D)$，只需对网络结构进行搜索，而候选结构的最优参数可直接在训练集上计算得到。

​		不幸的是，从所有可能的网络结构空间搜索最优贝叶斯网结构是一个 $NP$ 难问题，难以快速求解。有两种常用的策略能在有限时间内求得近似解：

- 第一种是贪心法，例如从某个网络结构出发，每次调整一条边 (增加、删除或调整方向)，直到评分函数值不再降低为止；

- 第二种是通过给网络结构施加约束来削减搜索空间，例如将网络结构限定为树形结构等。



### 推断

​		贝叶斯网训练好之后就能用来回答“查询”(query)，即通过一些属性变量的观测值来推测其他属性变量的取值。例如在西瓜问题中，若我们观测到西瓜色泽青绿、敲声浊响、根蒂蜷缩，想知道它是否成熟、甜度如何。这样通过已知变量观测值来推测待查询变量的过程称为“推断”(inference)，已知变量观测值称为“证据”(evidence)。

​		最理想的是直接根据贝叶斯网定义的联合概率分布来精确计算后验概率，不幸的是，这样的“精确推断”已被证明是 NP 难的；换言之，当网络结点较多、连接稠密时，难以进行精确推断，此时需借助“近似推断”，通过降低精度要求，在有限时间内求得近似解。在现实应用中，贝叶斯网的近似推断常使用吉布斯采样 (Gibbs sampling) 来完成，这是一种随机采样方法，我们来看看它是如何工作的。
​		令 $Q=\{Q_1,Q_2,...,Q_n\}$ 表示待查询变量，$E=\{E_1,E_2,...,E_k\}$ 为证据变量，已知其取值为 $e=\{e_1,e_2,...,e_k\}$。目标是计算后验概率 $P(Q=q\mid E= e)$，其中 $q=\{q_1,q_2,...,q_n\}$ 是待查询变量的一组取值。以西瓜问题为例，待查询变量为 $Q=\{好瓜,甜度\}$，证据变量为 $E=\{色泽,敲声,根蒂\}$ 且己知其取值为 $e= \{青绿,浊响,蜷缩\}$，查询的目标值是 $q=\{是,高\}$，即这是好瓜且甜度高的概率有多大。

​		如下图所示，吉布斯采样算法先随机产生一个与证据 $E=e$ 一致的样本 $q^0$ 作为初始点，然后每步从当前样本出发产生下一个样本。具体来说，在第 $t$ 次采样中，算法先假设 $q^t=q^{t-1}$，然后对非证据变量逐个进行采样改变其取值，采样概率根据贝叶斯网 $B$ 和其他变量的当前取值 (即 $Z$  = $z$ ) 计算获得。假定经过 $T$ 次采样得到的与 $q$ 一致的样本共有 $n_q$ 个，则可近似估算出后验概率
$$
P(Q=q\mid E=e)\simeq\frac{n_q}{T}\,\,.\tag{33}
$$
![吉布斯采样算法.png](https://github.com/Giyn/QG2020SummerTraining/blob/master/Pictures/NaiveBayes/%E5%90%89%E5%B8%83%E6%96%AF%E9%87%87%E6%A0%B7%E7%AE%97%E6%B3%95.png?raw=true)

​		实质上，吉布斯采样是在贝叶斯网所有变量的联合状态空间与证据 $E= e$ 一致的子空间中进行“随机漫步” (random walk)。每一步仅依赖于前一步的状态，这是一个“马尔可夫链” (Markov chain)。在一定条件下，无论从什么初始状态开始，马尔可夫链第 $t$ 步的状态分布在 $t→∞$ 时必收敛于一个平稳分布 (stationary distribution)；对于吉布斯采样来说，这个分布恰好是 $P(Q\mid E=e)$。因此，在T很大时，吉布斯采样相当于根据 $P(Q\mid E=e)$ 采样，从而保证了式 (33) 收敛于 $P(Q=q\mid E=e)$。

​		需注意的是，由于马尔可夫链通常需很长时间才能趋于平稳分布，因此吉布斯采样算法的收敛速度较慢。此外，若贝叶斯网中存在极端概率“0”或“1”，则不能保证马尔可夫链存在平稳分布，此时吉布斯采样会给出错误的估计结果。



### $EM$ 算法

​		在前面的讨论中，我们一直假设训练样本所有属性变量的值都已被观测到，即训练样本是“完整”的。但在现实应用中往往会遇到“不完整”的训练样本，例如由于西瓜的根蒂已脱落，无法看出是“蜷缩”还是“硬挺”，则训练样本的“根蒂”属性变量值未知。在这种存在“未观测”变量的情形下，是否仍能对模型参数进行估计呢？未观测变量的学名是“隐变量” (latent variable)。令 $X$ 表示已观测变量集，$Z$ 表示隐变量集，$\Theta$ 表示模型参数。若欲对 $\Theta$ 做极大似然估计，则应最大化对数似然
$$
LL(\Theta\mid X,Z)=\ln P(X,Z\mid \Theta)\,\,.\tag{34}
$$

> 由于“似然”常基于指数族函数来定义，因此对数似然及后续 $EM$ 迭代过程中一般是使用自然对数 $ln(·)$。

然而由于 $Z$ 是隐变量，上式无法直接求解。此时我们可通过对 $Z$ 计算期望，来最大化已观测数据的对数“边际似然” (marginal likelihood)
$$
LL(\Theta\mid X)=\ln P(X\mid \Theta)=\ln\sum_ZP(X,Z\mid\Theta)\,\,.\tag{35}
$$
​		$EM$ (Expectation-Maximization) 算法是常用的估计参数隐变量的利器，它是一种迭代式的方法，其基本想法是：若参数 $\Theta$ 已知，则可根据训练数据推断出最优隐变量 $Z$ 的值 ($E$ 步)；反之，若  $Z$ 的值已知，则可方便地对参数 $\Theta$ 做极大似然估计($M$ 步)。

>直译为“期望最大化算法”，通常直接称 $EM$ 算法。

​		于是，以初始值 $\Theta^0$ 为起点，对式 (35)，可迭代执行以下步骤直至收敛：

- 基于 $\Theta^t$ 推断隐变量 $Z$ 的期望，记为 $Z^t$；
- 基于已观测变量 $X$ 和 $Z^t$ 对参数 $\Theta$ 做极大似然估计，记为 $\Theta^{t+1}$；、

这就是 $EM$ 算法的原型。

​		进一步，若我们不是取 $Z$ 的期望，而是基于 $\Theta^t$ 计算隐变量 $Z$ 的概率分布 $P(Z\mid X,\Theta^t)$，则 $EM$ 算法的两个步骤是：

- $E$ 步 (Expectation)：以当前参数 $\Theta^t$ 推断隐变量分布 $P(Z\mid X,\Theta^t)$，并计算对数似然 $LL(\Theta\mid X,Z)$ 关于 $Z$ 的期望

$$
Q(\Theta\mid \Theta^t)=\mathbb{E}_{Z|X,\Theta^t}LL(\Theta\mid X,Z)\,\,.\tag{36}
$$

- $M$ 步 (Maximization)：寻找参数最大化期望似然，即

$$
\Theta^{t+1}=\mathop{\arg\max}_{\Theta}Q(\Theta\mid\Theta^t)\,\,.\tag{37}
$$

​		简要来说，$EM$ 算法使用两个步骤交替计算：第一步是期望 $(E)$ 步，利用当前估计的参数值来计算对数似然的期望值；第二步是最大化 $(M)$ 步，寻找能使 $E$ 步产生的似然期望最大化的参数值。然后，新得到的参数值重新被用于 $E$ 步，……直至收敛到局部最优解。

​		事实上，隐变量估计问题也可通过梯度下降等优化算法求解，但由于求和的项数将随着隐变量的数目以指数级上升，会给梯度计算带来麻烦；而EM算法则可看作一种非梯度优化方法。

> $EM$ 算法可看作用坐标下降 (coordinate descent) 法来最大化对数似然下界的过程。

---

Reference：《机器学习》
