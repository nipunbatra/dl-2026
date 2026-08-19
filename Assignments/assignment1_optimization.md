# Assignment 1 


## Q1 - Optimizers on Loss Surfaces

Implement the below optimiser functions yourself using pytorch/numpy. Do not use the built-in optimizer implementations from PyTorch.
- Gradient descent
- Momentum
- SGD
- Adam
- Minibatch-SGD 

Run each optimizer on the three loss surfaces below. Start from the given point and run for at most 1000 steps.  Use $\beta = 0.9$ for momentum, and $\beta_1 = 0.9$, $\beta_2 = 0.999$ for Adam. For SGD and minibatch-SGD, add noise to the gradient, for example $g \leftarrow g + \sigma\,\xi$, where $\xi \sim \mathcal{N}(0, I)$ and $\sigma$ sets the noise scale. If a path flies off-screen, halve $\eta$.

### Loss Surfaces

| # | Surface | $L(x,y)$ | Start |
|---|---|---|---|
| 1 | Bowl | $x^2 + y^2$ | $(-4, 4)$ |
| 2 | Ravine | $x^2 + 200y^2$ | $(-4, 3)$ |
| 3 | Saddle | $x^2 - y^2$ | $(-1.5, 0.001)$ |

For each surface, run every optimizer for at most 1000 steps and record each $(x, y)$ pair it visits. Draw the contour lines and animate the trajectories as moving dots. If a method does not converge within this limit, that is acceptable.

- Create 3 GIFs, one for each surface, with all optimizer paths overlaid, a legend, and a step counter.
- A small table showing, for each surface and optimizer (All 3 surfaces, and 5 optimizers), whether the method reached the minimum and how many steps it took. For the saddle, report how many steps it took to move clearly away from the centre.


## Q2 - Optimizers on Rosenbrock

Extend Q1 with Rosenbrock surface. Run on all 5 optimizers, following the instructions of Q1.

| # | Surface | $L(x,y)$ | Start |
|---|---|---|---|
| 1 | Rosenbrock | $(1 - x)^2 + 100(y - x^2)^2$ | $(-1.5, 1.5)$ |

- Produce a GIF (Rosenbrock, showing all 5 optimizers overlaid, a legend, and a step counter).
- Produce a table in the same format as Q1, covering all 5 optimizers on Rosenbrock, including whether the method reached the minimum and how many steps it took.
- For which optimizers, and why, is Rosenbrock (Q2) harder to optimize than the three surfaces from Q1? Reference your results from both questions.


## Q3 - Learning-rate Schedules with Adam

Use **Adam** on the Rosenbrock surface from Q1 and Q2, and vary the **learning-rate schedule** $\eta_t$.

### Schedules to compare
Implement $\eta_t$ for the following schedules yourself using PyTorch and NumPy:
- **Constant Learning Rate** 
$\eta_t = \eta$; 
- **Step Decay**, where the learning rate is reduced by a factor of $0.1$ every $K$ steps; 
- **Exponential Decay** $\eta_t = \eta_0\,\gamma^t$;
- **Cosine annealing** $\eta_t = \eta_{\min} + \frac{1}{2}(\eta_0 - \eta_{\min})\left(1 + \cos\left(\frac{\pi t}{T}\right)\right)$; and 
- **Linear warmup plus cosine decay**.

$$
\eta_t =
\begin{cases}
\dfrac{t}{T_{\mathrm{warmup}}}\,\eta_0, & t \le T_{\mathrm{warmup}}, \\
\eta_{\min} + \dfrac{1}{2}(\eta_0 - \eta_{\min})\left(1 + \cos\left(\dfrac{\pi (t - T_{\mathrm{warmup}})}{T - T_{\mathrm{warmup}}}\right)\right), & t > T_{\mathrm{warmup}}.
\end{cases}
$$



- Create a GIF showing the schedule trajectories on the Rosenbrock contours, with a side panel or second GIF showing the `η_t` curves.
- A plot of loss versus step for each schedule on Rosenbrock.
- A short write-up of the schedules, including which one performed best and whether warmup improved the early steps.


## Q4 - Dropout on FashionMNIST

Use **FashionMNIST** to study the effect of dropout on a small MLP.

You can load the dataset in PyTorch with:

```python
from torchvision import datasets, transforms

transform = transforms.ToTensor()

train_dataset = datasets.FashionMNIST(
	root="data",
	train=True,
	download=True,
	transform=transform,
)

test_dataset = datasets.FashionMNIST(
	root="data",
	train=False,
	download=True,
	transform=transform,
)
```

Use a small subset, for example 5,000 training images and 1,000 test images, and a simple MLP. First train a plain MLP with no regularisation. Then compare it with the same MLP using dropout. Train each model for 50 epochs. You can use pytorch optimisers in this question.

- Plot the training and test curves for both models. Report accuracy and F1 score at each epoch.
- Repeat the dropout experiment with dropout probabilities of $0.1$, $0.25$, $0.5$, and $0.75$, and plot the training and test curves for each setting.
- Comment on which dropout probability worked best, and on what happens to the gap between training and test performance as the dropout probability increases.

---

## Q5 - Lamp placement in a dark room

Place **three lamps** in a unit-square room so that the room is as bright as possible, while keeping the lamps from collapsing to the same point.

Let the lamp positions be $l_1, l_2, l_3 \in [0, 1]^2$. A lamp at position $l$ contributes brightness $B_l(p) = \exp\left(-\frac{\|p - l\|^2}{2\sigma^2}\right)$ at room location $p$. The total brightness is the sum over the three lamps.

### Understanding the brightness term

$B_l(p)$ says how much light a lamp at $l$ throws onto a point $p$. It is a Gaussian bump centred on the lamp: brightest at the lamp itself and falling off with distance. The parameter $\sigma$ controls how far the light reaches — a large $\sigma$ is a dim lamp that spreads light widely, a small $\sigma$ is a focused spotlight.

#### Reading $\|p - l\|^2$

Both $p = (p_x, p_y)$ and $l = (l_x, l_y)$ are points in the room, so $p - l$ is a vector, not a number: you subtract coordinate by coordinate. Then $\|\cdot\|^2$ is its squared length, which by Pythagoras is

$$
\|p - l\|^2 = (p_x - l_x)^2 + (p_y - l_y)^2
\quad\text{e.g.}\quad
p = (0.5, 0.5),\ l = (0.3, 0.3) \ \Rightarrow\ 0.2^2 + 0.2^2 = 0.08 .
$$

This is the **squared** distance, so there is no square root to take. The same rule applies to $\|l_i - l_j\|^2$ in the repulsion term, with two lamps in place of a lamp and a room point.

#### Worked example

Worked example with $\sigma = 0.25$ and a lamp at $l = (0.3,\ 0.3)$. Note $2\sigma^2 = 2(0.25)^2 = 0.125$:

| room point $p$ | $\|p - l\|^2$ | $B_l(p) = \exp\left(-\frac{\|p-l\|^2}{2\sigma^2}\right)$ |
|---|---|---|
| $(0.3,\ 0.3)$ — at the lamp | $0$ | $\exp(0) = 1.000$ |
| $(0.5,\ 0.5)$ — room centre | $0.2^2 + 0.2^2 = 0.08$ | $\exp(-0.08 / 0.125) = 0.527$ |
| $(1.0,\ 1.0)$ — far corner | $0.7^2 + 0.7^2 = 0.98$ | $\exp(-0.98 / 0.125) = 0.000$ |

so this lamp lights its own neighbourhood well, gives the centre about half brightness, and leaves the opposite corner essentially dark. With three lamps you add the three values at each point: if a point receives $0.53$ from one lamp, $0.40$ from another and $0.02$ from the third, its total brightness is $0.53 + 0.40 + 0.02 = 0.95$.

### Understanding the repulsion term

You may use a repulsion term of the form $R(l_1, l_2, l_3) = \sum_{i<j} \exp\left(-\frac{\|l_i - l_j\|^2}{2\rho^2}\right)$.

This is the same Gaussian shape, but measured between **pairs of lamps** rather than between a lamp and a room point, and it is *subtracted*. It is large when two lamps are close and near zero when they are far apart, so subtracting it penalises lamps that pile up on the same spot. The sum $\sum_{i<j}$ runs over the three distinct pairs $(1,2)$, $(1,3)$, $(2,3)$.

With $\rho = 0.2$, the penalty for a single pair of lamps a distance $d$ apart is:

| $d$ | 0.05 | 0.1 | 0.3 | 0.5 | 0.7 |
|---|---|---|---|---|---|
| penalty | 0.969 | 0.883 | 0.325 | 0.044 | 0.002 |

So two lamps almost on top of each other cost nearly $1$ each, while two lamps half a room apart cost almost nothing. $\lambda$ sets how strongly this matters relative to brightness.

### The full objective

Define the room objective as the average brightness over all points in the room grid. The grid $\mathcal{G}$ is just a set of sample points covering the room — for example a $100 \times 100$ lattice over $[0,1]^2$, so $|\mathcal{G}| = 10{,}000$ — used to approximate "brightness averaged over the whole room". The objective is

$$
J(l_1,l_2,l_3) = \frac{1}{|\mathcal{G}|} \sum_{p \in \mathcal{G}} \sum_{k=1}^3 B_{l_k}(p) - \lambda R(l_1,l_2,l_3).
$$

### Choosing the constants

$\sigma = 0.25$, $\rho = 0.20$, $\lambda = 1.0$ is a good starting point and will give sensible-looking results. You are encouraged to vary them and see what changes:

- **$\sigma$** — how far each lamp throws light. Large $\sigma$ makes every placement look similar; small $\sigma$ leaves dark gaps between the lamps.
- **$\rho$** — the range over which lamps push each other away.
- **$\lambda$** — how much the lamps care about spreading out versus lighting the room. Set $\lambda = 0$ to see what happens with no repulsion at all.

Feel free to comment on anything interesting you find here, though only the run with your chosen settings needs to be reported in full.


Use any optimiser (SGD, Momentum, Adam, any you like) to maximize $J$ from a random start. 

- The brightness map of the room before and after optimization.
- An animated GIF of the three lamps moving to their final positions.
- Run a few random seeds and report whether they agree on the final placement.
- Create GIFs for 4, 6 and 8 lamps as well.


### Things to watch out for:

- Optimisers **minimise**, so call `.backward()` on $-J$ rather than on $J$.
- Nothing in $J$ stops a lamp from wandering outside the room. You may have to clamp the positions back into $[0,1]^2$ after each step or figure out any other formulation to stay inside the bound.
- $J$ is not convex, so the result depends on where you start.
