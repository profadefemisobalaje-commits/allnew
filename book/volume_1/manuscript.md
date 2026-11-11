# Preface

Artificial intelligence and robotics meet wherever a machine must make a decision that matters in the physical world. A model may classify an image correctly, yet a robot using that model can still fail because its camera is blurred, its clock is late, or its brakes are undersized. Engineering therefore requires more than an impressive algorithm: it requires a chain of evidence from a problem statement to a system that behaves acceptably in its intended environment.

This volume introduces six foundations of that chain. The chapters begin with artificial intelligence and the physical structure of robots, then develop machine learning, computer vision, natural language processing, and feedback control. Mathematics is presented as a language for making assumptions explicit. Worked examples are deliberately small enough to check by hand; the reader should build confidence on these examples before trusting larger software systems.

**Editorial status.** This PDF is an introductory manuscript, not the requested complete Volume I. The six chapters are substantially shorter than the specified minimum of 20,000 words each. Its references are recommended starting points, not a verified comprehensive bibliography, and it has not undergone independent academic, technical, or publication review. It should not be represented as a final encyclopedia volume.

# How to use this volume

Read the first two chapters together: an intelligent agent is an abstract decision-maker, while a robot must also obey physical limits. Chapter 3 introduces the data and evaluation ideas used by Chapters 4 and 5. Chapter 6 can be studied alongside Chapter 2. Keep a notebook of assumptions, units, expected results, and sources. Recalculate each worked example before changing the numbers. A computer can run an experiment quickly, but it cannot decide whether the experiment answers a useful question.

A suitable background is elementary algebra and comfort with simple Python. Where calculus appears, the meaning of the result is explained in words. Experiments described here are illustrative; physical work requires supervision, a risk assessment, an appropriate power supply, guarding, and a tested emergency-stop arrangement. Software examples alone are not a safety system.

# 1. Introduction to Artificial Intelligence

## What makes a system intelligent?

A thermostat and a route planner both respond to information, but they work at different levels of complexity. The thermostat may compare a measured temperature with a target and switch a heater. A route planner considers many possible sequences of actions before choosing one. Artificial intelligence (AI) studies and builds computational systems that perform tasks associated with perception, reasoning, learning, language, or decision-making. No single definition settles every debate about intelligence. For engineering, the useful question is narrower: what task must the system perform, under which conditions, and how will success be measured?

Modern AI has roots in formal logic, statistics, computing, neuroscience, and control. Early research explored symbolic reasoning and search. Expert systems later encoded specialist rules; statistical methods and machine learning became increasingly important as data and computing resources grew. Contemporary systems combine these traditions in different proportions. A system that performs one task well is not thereby guaranteed to possess general human capabilities.

## Agents and environments

An agent receives observations and selects actions. Its environment includes everything relevant to the consequences of those actions. A warehouse robot, for example, observes ranges and images, commands wheel motors, and works among shelves and people. The engineer must decide what to measure: completed deliveries, collision rate, energy use, or a weighted combination. A performance measure that rewards speed alone can encourage unsafe behavior.

An environment is fully observable only when the information available to the agent is sufficient to determine the relevant state. A camera blocked by a box makes an aisle partially observable. The world may also be stochastic: the same motor command can lead to different results when floor friction changes. An agent's internal estimate of the situation is therefore not necessarily the situation itself. Confidence in an estimate should not be confused with proof that it is correct.

## Search as structured problem solving

A search problem specifies an initial state, possible actions, a transition model, a goal test, and, when relevant, action costs. Consider four locations with edges S–A, S–B, A–G and B–G. If each move costs one unit, breadth-first search explores by increasing number of moves and finds a two-edge route from S to G. It is complete on a finite graph when repeated states are handled, and it gives a shortest path in number of edges when all edge costs are equal. If costs differ, uniform-cost search instead expands the frontier state with lowest accumulated cost.

A* uses the priority f(n) = g(n) + h(n). Here g(n) is the cost of the path found so far to node n, and h(n) estimates the remaining cost to the goal. Suppose g(A) = 3 and h(A) = 2, while g(B) = 2 and h(B) = 5. The priorities are 5 and 7, so A is selected first. A heuristic is admissible when it never overestimates the true remaining cost. Optimality claims also depend on the algorithm's termination and graph-search rules; for a standard closed-list implementation without reopening nodes, consistency of the heuristic is a common sufficient condition. An estimated straight-line distance can be useful when travel cost is distance and obstacles can only make a route longer.

## Knowledge, uncertainty, and learning

A rule such as “if the charging cable is attached, do not drive” makes a design constraint explicit. Symbolic rules are inspectable, but a rule base can become difficult to maintain and may not cover unexpected circumstances. Probability provides a different tool: it expresses uncertainty about events under a model and available evidence. For instance, if a diagnostic test has a false-positive rate, a positive result is not automatically proof of a fault. Base rates matter as well as test accuracy.

Learning systems adjust a model using data or experience. Supervised learning uses examples with target labels; unsupervised learning looks for structure without those labels; reinforcement learning studies decisions informed by rewards and consequences. Each choice implies a different source of feedback. Learning can complement rules, but a learned prediction must be evaluated for the population and operating conditions in which it will be used.

## Applications and limits

AI can assist with medical image review, translate text, help sort goods, and estimate equipment faults. The same model may perform differently across hospitals, languages, cameras, or time periods. A deployment decision should identify whose errors matter, how a person can challenge or override an output, and how the system will be monitored after release. Human oversight is meaningful only when the operator has sufficient information, authority, and time to act.

A language model may produce a fluent but false explanation. A vision model may be confident about an unfamiliar object. Neither fluency nor confidence alone establishes correctness. The responsible approach is to specify the claim, test against relevant evidence, record failures, and provide a safe response when uncertainty is too high.

## Review and investigation

1. Describe the observations, actions, environment, and performance measures for an automated crop-inspection robot. Which important variables are hidden?
2. Construct a weighted graph where the route with the fewest edges is not the least-cost route. Explain why breadth-first and uniform-cost search may return different paths.
3. A heuristic returns zero for every node. What does A* prioritize? What information has the heuristic failed to provide?
4. Propose a way to detect a harmful change in performance after deployment without collecting unnecessary personal information.

# 2. Robotics Fundamentals

## A robot is an integrated physical system

A robot is commonly understood as a programmable machine that senses or otherwise obtains information and acts on the physical world. Its capabilities arise from the interaction of structure, actuators, sensors, computation, power, and control. A robotic arm attached to a workbench has a different workspace and risk profile from a mobile robot in a corridor. Both can use AI, but neither requires a learning model in every subsystem.

Industrial manipulators, mobile platforms, aerial vehicles, surgical devices, and agricultural robots are designed around different tasks. Comparisons require precise requirements: payload, reach, speed, accuracy, repeatability, operating environment, and acceptable risk. Accuracy describes closeness to a desired value; repeatability describes how consistently a system returns to the same result. A robot can be repeatable yet consistently miss the target because of calibration error.

## Links, joints, and motion

A manipulator can be described as links connected by joints. A revolute joint rotates; a prismatic joint translates. A degree of freedom is an independent coordinate needed to describe a permitted motion. Count carefully: the number of motors need not always equal the number of independent degrees of freedom, because mechanisms can be coupled.

Consider a planar arm with two rigid links of lengths L1 and L2. Let the first joint angle be θ1, measured from the horizontal, and let the second angle θ2 be relative to the first link. The tool position is x = L1 cos(θ1) + L2 cos(θ1 + θ2), y = L1 sin(θ1) + L2 sin(θ1 + θ2). Here x and y are coordinates in the base frame. For L1 = 1 m, L2 = 0.5 m, θ1 = 0°, and θ2 = 90°, the tool is at (1, 0.5) m. This is a forward-kinematics calculation: joint positions are known and tool position is found. Real mechanisms also have backlash, flex, joint limits, and calibration errors that this simple model omits.

## Actuators, transmissions, and power

Electric motors convert electrical energy into mechanical motion. A DC motor, a stepper motor, and a servo system are not interchangeable labels: a servo system generally includes a motor, feedback, and a controller. Gears can trade output speed for torque, but introduce losses, inertia, and possibly backlash. Pneumatic actuators offer a different combination of speed, compliance, and infrastructure requirements; hydraulic systems can provide high forces but bring leakage and maintenance concerns.

Torque is the turning effect of a force. In the simple perpendicular case, τ = F r, where τ is torque in newton-metres, F is force in newtons, and r is moment arm in metres. A 10 N load at 0.2 m produces 2 N·m of static torque about the joint. This is not a complete motor specification: acceleration, link mass, friction, gearbox efficiency, duty cycle, orientation, and a justified safety margin must also be considered.

## Sensors and uncertainty

An encoder measures movement of a shaft or joint, while a camera or range sensor provides information about the outside world. An inertial measurement unit senses angular velocity and acceleration; estimating position from these readings alone can accumulate substantial drift. Sensors have finite resolution and can be biased, noisy, delayed, or out of range. Calibration relates measurements to physical quantities and must be checked under appropriate conditions.

Suppose a distance sensor reports 0.95 m when a reference measurement is 1.00 m. The signed error is −0.05 m. A single measurement does not establish a systematic bias: take repeated readings at multiple distances, report the reference method and uncertainty, and examine whether the discrepancy varies with range or surface material.

## Architecture and safety

A common architectural description is sense, estimate, plan, and act, repeated as new measurements arrive. This is a conceptual decomposition rather than a promise that every robot runs a single sequential loop. A fast low-level motor controller can operate alongside a slower planner. Communication delay and missed deadlines can cause a correct decision to arrive too late.

Safety starts with identifying hazards: crushing, unexpected motion, electrical energy, dropped loads, stored pneumatic pressure, and interactions with people. Reducing risk may require guarding, safe separation, power isolation, suitable safety-rated components, and validated procedures. An emergency stop is a complementary protective measure, not a substitute for a risk assessment or all other protective measures. Consult applicable regulations and relevant standards for the specific machine and jurisdiction.

## Review and investigation

1. Sketch a mobile robot and label power, computation, sensors, actuators, transmission, and an emergency-stop arrangement. Explain what happens when a sensor fails.
2. For the two-link arm, calculate the position when both joint angles are zero. Explain why the answer has the units of length.
3. A gripper repeatedly stops 3 mm to the left of its target. Distinguish repeatability from accuracy and propose a calibration experiment.
4. Compare the actuator requirements of a lightweight educational arm and a continuously operating industrial gripper. Include duty cycle and maintenance.

# 3. Machine Learning

## The learning problem

Machine learning uses data or experience to fit a model for a task. In supervised learning the dataset contains inputs x and associated targets y; the model predicts a target for a new input. A regression model predicts a numerical quantity such as energy consumption. A classifier predicts categories such as acceptable or defective. A model does not automatically discover causal relationships: a useful prediction can arise from a correlation that later changes.

Consider predicting motor current from load. If all training measurements were collected at one temperature, a model may behave poorly at another. Record how examples were sampled, what the labels mean, and whether important operating conditions are represented. Missing data, mislabeled samples, and changes in sensor placement can matter more than the choice between two sophisticated algorithms.

## Training, validation, and test sets

The training set fits model parameters. The validation set supports choices such as features, model family, and hyperparameters. The test set estimates performance after those choices are fixed. If repeated measurements from one machine are divided randomly across all three sets, the model may benefit from machine-specific signatures. A split by machine, site, person, or time can better match the deployment question. Any preprocessing that learns from data, including scaling and imputation, must be fitted using the training portion within each split to avoid leakage.

A test estimate has uncertainty. Twenty examples cannot provide the same precision as a large, representative sample. Report the number and nature of examples, the metric, and important subgroup results; do not describe a single score as a universal property of the model.

## Linear regression worked by hand

A simple model is ŷ = wx + b. The symbol x denotes an input, w a slope, b an intercept, and ŷ the predicted output. For points (1, 3), (2, 5), and (3, 7), w = 2 and b = 1 give predictions 3, 5, and 7. Mean squared error is MSE = (1/n) Σ(yᵢ − ŷᵢ)², where n is the number of examples, yᵢ is a measured target, and ŷᵢ is its prediction. The errors are all zero on these three points, so the training MSE is zero. This does not prove that future predictions will be accurate.

Suppose a different model predicts 2, 5, and 8. Its residuals y − ŷ are 1, 0, and −1; the MSE is (1 + 0 + 1)/3 = 2/3. Squaring penalizes large errors more strongly and gives the metric squared target units. Root mean squared error restores the units of the target, but can still conceal unequal errors across operating regimes.

## Classification and trade-offs

A confusion matrix separates true positives (TP), false positives (FP), false negatives (FN), and true negatives (TN), relative to a stated positive class. Precision = TP/(TP + FP) asks what fraction of positive predictions were correct. Recall = TP/(TP + FN) asks what fraction of actual positives were found. With TP = 40, FP = 10, FN = 20 and TN = 930, precision is 40/50 = 0.80 and recall is 40/60 ≈ 0.667. Accuracy is 970/1000 = 0.97. The apparently high accuracy hides the missed positive cases because negatives are common.

A decision threshold changes the balance between false alarms and missed cases. Select it using a validation set and the consequences of errors; then evaluate the fixed threshold on separate test data. When the relevant denominator is zero, the corresponding metric needs an explicit convention rather than an unqualified numerical claim.

## Unsupervised learning and generalization

Clustering groups examples according to a chosen similarity measure. In k-means, an algorithm alternates between assigning points to a nearest centroid and updating centroids to the means of their assigned points. Results depend on scaling, initialization, the number of clusters, and the distance measure. A cluster is not automatically a meaningful real-world category, and the method can converge to a local rather than global optimum.

Overfitting occurs when a model captures details specific to the training set that do not transfer to new cases. Underfitting occurs when it cannot capture a relevant pattern even on the training data. Regularization, simpler models, suitable data, and careful validation can help, but none replaces a representative test of the actual task.

## Laboratory and review

Use the following standard-library Python fragment to verify the classification example. The assertions serve as small regression tests; they do not validate a deployed model.

```python
tp, fp, fn, tn = 40, 10, 20, 930
precision = tp / (tp + fp)
recall = tp / (tp + fn)
accuracy = (tp + tn) / (tp + fp + fn + tn)
assert abs(precision - 0.8) < 1e-12
assert abs(recall - 2/3) < 1e-12
assert abs(accuracy - 0.97) < 1e-12
print(f"precision={precision:.3f}, recall={recall:.3f}, accuracy={accuracy:.3f}")
```

1. Explain why a random row split can exaggerate performance when many rows come from the same robot.
2. Recalculate precision and recall if five false positives become true negatives and all other counts remain unchanged.
3. Plan a dataset for predicting motor faults. Describe consent where appropriate, label verification, a baseline, and a test split that reflects future use.

# 4. Computer Vision

## From light to an array

Computer vision seeks information about a scene from images or video. A camera records a sampled, quantized response to light; the array is not the scene itself. Illumination, exposure, lens distortion, sensor noise, and movement all influence the captured data. A dark object under strong illumination can produce a similar pixel value to a lighter object in shadow. Consequently, an algorithm needs assumptions about the acquisition process as well as the image contents.

A grayscale image can be represented as I(r, c), the intensity at row r and column c. A color image usually has multiple channels. The numeric range depends on the representation: an unsigned 8-bit channel commonly uses integers from 0 to 255. Coordinate conventions vary, so specify whether the first index denotes a row or an x-coordinate and where the origin is located.

## Filtering and edges

A spatial filter computes a new value from a neighborhood of pixels. For a simple one-dimensional example, take values 2, 5, and 8 and average them with weights 1/3 each: the output is 5. Smoothing reduces some random variation but can blur fine details and boundaries. A median filter replaces the central value by the median in a neighborhood and can be useful for isolated impulse noise; it does not remove all forms of noise.

An edge detector looks for rapid image-intensity change. In a one-dimensional sequence [10, 10, 30, 30], adjacent differences are [0, 20, 0], showing a transition between the second and third samples. Real image gradients have horizontal and vertical components, and an intensity edge need not be an object boundary: it may be a shadow, reflection, or texture. Threshold choice trades missed edges against spurious detections.

## Segmentation, detection, and recognition

Segmentation assigns pixels to regions. A binary threshold may classify a pixel as foreground if its intensity exceeds a chosen value; it works only if the selected intensity rule separates the relevant regions well enough. Semantic segmentation assigns a class to each pixel, whereas instance segmentation distinguishes individual objects of the same class. Detection typically identifies objects with a class and a bounding box; classification assigns a label to an image or region. These are related but different tasks, and their evaluation must match the output.

For a detected box, intersection over union (IoU) is the area of overlap divided by the area of the union of the predicted and reference boxes. If each box has area 100 square pixels and their overlap is 60 square pixels, the union is 100 + 100 − 60 = 140 and IoU = 60/140 ≈ 0.429. A higher IoU indicates better geometric agreement under this measure, but it does not by itself establish that the class label is correct.

## Geometry and calibration

In an ideal pinhole camera, a point with camera-frame coordinates (X, Y, Z), with Z > 0, projects to u = fₓX/Z + cₓ and v = fᵧY/Z + cᵧ. The quantities fₓ and fᵧ are focal lengths expressed in pixel units; cₓ and cᵧ give the principal point in pixels. For fₓ = 500 pixels, X = 0.2 m, Z = 2 m, and cₓ = 320 pixels, u = 370 pixels. The ratio X/Z is dimensionless. Real lenses distort images, and calibration estimates parameters from observations; uncertainty and calibration quality matter for measurement.

One image does not generally determine absolute depth without additional assumptions or information. Stereo cameras, known object dimensions, motion, structured light, and other sensors can add constraints. Later robot-vision work connects these estimates to coordinate transforms and action.

## Design and evaluation

For an inspection task, begin with controlled illumination and a camera positioned to reveal the defect. Acquire images representing good and defective examples, normal variation, and foreseeable failure conditions. Separate data by production run where appropriate. Evaluate detection on a held-out set with reference labels, then review false negatives and false alarms with domain specialists. A system that works only on one bench is not necessarily ready for an operating factory.

Image datasets may contain identifiable people, locations, or confidential processes. Minimize collection, control access, and establish a suitable legal and ethical basis. Operational monitoring should include image-quality checks, not just the classifier's confidence.

## Review and investigation

1. Give an example where a brightness threshold fails because of a shadow. Suggest a change to the acquisition setup.
2. Calculate IoU if two boxes have areas 50 and 70 and overlap by 20 square pixels.
3. In the pinhole model, what happens to u − cₓ when Z doubles and all other terms stay fixed?
4. Design a test that measures how motion blur affects defect detection. State the controlled variables and the result you would record.

# 5. Natural Language Processing

## Language as an engineering problem

Natural language processing (NLP) builds systems that process human language. Language is not a simple codebook. A word may have several meanings, speakers omit shared context, and the same request can be phrased in many ways. “Move the box beside the door” can refer to more than one box or door. A robot acting on that sentence should ask for clarification when the ambiguity matters, rather than quietly selecting an arbitrary interpretation.

A corpus is a collection of language examples. Its sources, languages, dialects, permissions, and labeling procedures affect what a model can learn and who it serves. Text may contain names, medical details, or other sensitive information. Data minimization and access controls are part of the design, not an afterthought.

## Tokens and representations

Tokenization divides a string into units for processing. Depending on the method, a token can be a word, a character, or a subword. No single tokenization is best for all languages and tasks. Converting everything to lowercase may simplify a topic classifier but can destroy useful distinctions such as proper names or product identifiers.

A bag-of-words representation counts tokens while discarding their order. For the vocabulary [robot, moves, stops], “robot moves” becomes [1, 1, 0], while “robot stops” becomes [1, 0, 1]. This representation cannot distinguish sentences with the same counts but different word order. N-grams preserve a limited amount of local order; embeddings map tokens or sequences to vectors whose learned structure may help with similarity, though geometric closeness should not be treated as an infallible measure of meaning.

## Probability and language models

A language model assigns probabilities to sequences. By the chain rule, P(w₁, w₂) = P(w₁)P(w₂ | w₁), where w₁ and w₂ are tokens and the vertical bar means “given.” If P(robot) = 0.1 and P(moves | robot) = 0.4, the joint probability of the two-token sequence under this simple model is 0.04. A bigram model approximates each next-token probability using the previous token. It cannot directly represent all long-range dependencies, and unseen bigrams require smoothing or another treatment.

Modern transformer models use attention to combine information across token positions. Their output probabilities are produced from learned parameters and context; generating plausible continuations is not equivalent to verifying a statement against the world. Systems that use such models for consequential tasks need independently checked evidence, restrictions on actions, and clearly defined human responsibility.

## Classification, extraction, and evaluation

A sentiment classifier assigns a category to text, while named-entity recognition identifies spans such as names or places. For example, an entity system might mark “Lagos” in a transport request as a location. Correctness depends on both the span boundaries and the assigned class. A model can be right about the general topic and still misidentify the destination.

Evaluate on examples representative of actual use, including paraphrases, spelling errors, relevant languages, and ambiguous requests. Splitting near-duplicate messages across training and test sets can overstate generalization. For an action-taking interface, report not only classification metrics but also the rate of unsafe or misunderstood commands, and test the behavior when the system declines or requests clarification.

## Language and robots

A language instruction must be grounded in the robot's environment: “the red cup” should be connected to an observed candidate object and a reachable location. Perception can be wrong, and a correct parse may still describe an unsafe action. A robust interaction confirms critical targets, checks permissions and physical constraints, and provides a way to stop. The system should tell users when it cannot reliably resolve a request rather than inventing certainty.

## Review and investigation

1. Show two sentences with identical bag-of-words counts but different meanings. Explain what information is lost.
2. A language model assigns P(open) = 0.2 and P(door | open) = 0.3. Compute the probability of that two-token sequence under the given model.
3. Design a clarification question for an instruction involving two visually similar objects. Explain when the robot should refuse to act.
4. Compare evaluation of an entity extractor with evaluation of a complete robot instruction system.

# 6. Control Systems

## From intention to feedback

Control engineering studies how to influence the behavior of dynamic systems. A controller may keep a motor at a desired speed or guide a robot arm to a position. In open-loop control, the command is issued without using a measurement of the resulting output to correct it. In closed-loop control, the measured output is compared with a reference and the difference informs subsequent action. Feedback can reduce some disturbances and model errors, but poor feedback design can also produce oscillation or instability.

Let r(t) be the desired output, y(t) the measured output, and e(t) = r(t) − y(t) the error at time t. If the desired speed is 10 revolutions per second and the measured speed is 8, the error is 2 revolutions per second. The sign convention matters: reversing the subtraction without adjusting the controller can turn negative feedback into positive feedback.

## A simple dynamic model

A first-order plant can be written τ dy/dt + y = Ku, where y is output, u is input, K is the steady-state gain, and τ is a positive time constant. The units of K depend on the units of output and input; τ is measured in seconds when time is measured in seconds. For a constant input u and a stable plant at equilibrium, dy/dt = 0, so y = Ku. With K = 2 and u = 3, the steady-state output is 6 in the chosen output units.

For a step from zero initial output to a constant input, the ideal response is y(t) = Ku[1 − exp(−t/τ)]. At t = τ, the response has reached approximately 63.2% of its final value. This model is useful only when its assumptions approximate the real plant; actuator saturation, delay, changing load, and nonlinear friction may require a richer description.

## Proportional and integral action

A proportional controller uses u(t) = Kₚe(t), where Kₚ is proportional gain. Increasing gain can produce a stronger response to error, but too much gain may cause oscillation or instability. For a unity-feedback first-order plant with steady-state gain K and no input saturation, the steady-state error for a constant reference r under proportional control is eₛₛ = r/(1 + KKₚ). If K = 2, Kₚ = 3 and r = 7, the error is 1 in output units. This formula depends on the stated structure and equilibrium assumptions; it is not a universal PID rule.

Integral action accumulates error over time. In continuous time, a standard PID expression is u(t) = Kₚe(t) + Kᵢ∫e(t)dt + K𝒹 de(t)/dt. The integral gain is Kᵢ and derivative gain is K𝒹. The integral term can remove steady-state error for suitable stable systems, while derivative action responds to the rate of change of error and can amplify measurement noise. The choice of units for each gain follows from the units of error, command, and time.

Actuators have limits. When a command is saturated, an unconstrained integral term may continue to grow, causing integral windup and a long recovery. Anti-windup methods limit or correct this accumulation. Practical implementations often filter derivative action and may differentiate the measurement rather than the reference to reduce derivative kick on setpoint changes.

## Stability, sampling, and implementation

A stable response does not grow without bound after a bounded disturbance under the relevant stability definition and model assumptions. For a linear time-invariant continuous-time model, poles in the left half of the complex plane are a standard condition for asymptotic internal stability. A model is not the physical plant: an unmodeled delay, unexpected load, or broken sensor can invalidate a theoretical conclusion.

Digital controllers measure and update at discrete times. A simple discrete integral approximation is Iₖ = Iₖ₋₁ + KᵢeₖΔt, with sample interval Δt. Variable timing changes the accumulated contribution unless actual elapsed time is accounted for. Choose a sampling rate appropriate to system dynamics, check timing and filtering, and validate on a safe test setup. No fixed sampling rate is sufficient for all plants.

## A cautious experiment

Start with a simulated first-order plant and a proportional controller. Record the reference, output, error, input, time step, and gain. Increase gain in small steps and compare rise time, overshoot, and steady-state error. Repeat with an actuator limit. Only after documenting model assumptions and conducting a physical risk assessment should a qualified team consider testing on hardware. Disconnecting software commands does not necessarily remove stored energy or bring moving equipment to a safe state.

## Review and investigation

1. Distinguish a disturbance from measurement noise and give a robotics example of each.
2. For the first-order model with K = 1.5 and constant input 4, find the equilibrium output. State the assumptions.
3. Explain integral windup using a motor that cannot deliver the requested torque.
4. Draw a negative-feedback loop and label reference, error, controller, plant, measurement, and feedback direction.

# Selected reading

The following established texts are starting points for further study; they are not a comprehensive bibliography for a finished volume. Consult the editions available to you and verify details before publication.

- Russell, Stuart, and Peter Norvig. *Artificial Intelligence: A Modern Approach*. 4th ed. Pearson, 2021. Chapters on agents, search, and learning.
- Lynch, Kevin M., and Frank C. Park. *Modern Robotics: Mechanics, Planning, and Control*. Cambridge University Press, 2017. Kinematics and robot mechanics.
- Bishop, Christopher M. *Pattern Recognition and Machine Learning*. Springer, 2006. Statistical foundations and model evaluation.
- Szeliski, Richard. *Computer Vision: Algorithms and Applications*. 2nd ed. Springer, 2022. Image formation, features, and recognition.
- Jurafsky, Daniel, and James H. Martin. *Speech and Language Processing*. 2nd ed. Pearson, 2009. Language processing and statistical models.
- Åström, Karl J., and Richard M. Murray. *Feedback Systems: An Introduction for Scientists and Engineers*. Princeton University Press, 2008. Modeling, feedback, and stability.

# Glossary

**Agent:** A system that selects actions using information from an environment.

**Calibration:** A procedure relating an instrument's indications to reference quantities, with attention to uncertainty.

**Generalization:** Performance on relevant examples not used to fit or select the model.

**Grounding:** Connecting a symbol or linguistic expression to entities or actions in a context.

**Heuristic:** An estimate used to guide a search; its formal properties depend on how it is defined.

**Model:** A simplified mathematical or computational representation used for a specified purpose.

**Sensor:** A device that produces a signal related to a physical quantity.

**Stability:** A property describing how a system responds to perturbations or inputs, under a specified definition.

**Validation set:** Data used to make modeling choices before final testing.
