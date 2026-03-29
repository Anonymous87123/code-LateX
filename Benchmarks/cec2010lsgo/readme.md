符号规定：
D = dimension = 1000
m = 50
i = 1,..,D
x = (x1, x2,···, xD):变量
o = (o1, o2,···, oD):移位向量
z = x - o = (z1, z2,···, zD)
P = (p_1, p_2,···, p_D):置换向量
t = P(z) = (t_1, t_2,···, t_D):对z按照置换向量P进行置换
rot:函数前缀，表示对变量进行旋转操作

基本函数：
sphere: F(x) = Σ(x_i^2)
elliptic: F(x) = Σ(10^(6*(i-1)/(D-1)) * x_i^2)
rastrigin: F(x) =  Σ(x_i^2 - 10 * cos(2 * π * x_i)+10)
ackley: F(x) = -20 * exp(-0.2 * sqrt(1/D * Σ(x_i^2))) - exp(1/D * Σ(cos(2 * π * x_i))) + 20 + exp(1)
schwefel: F(x) = Σ(Σ(x_j, j=1,...,i), i=1,...,D)^2
rosebrock: F(x) = Σ(100*(x_i^2 - x_{i+1})^2 + (x_i - 1)^2)

20个函数配置：
F1：z=x-o,elliptic(z)
F2：z=x-o,rastrigin(z)
F3：z=x-o,ackley(z)
F4：z=x-o,t=P(z),rot_elliptic(t1,..,t_m)*10^6+elliptic(t_m+1,..,t_D)
F5：z=x-o,t=P(z),rot_rastrigin(t1,..,t_m)*10^6+rastrigin(t_m+1,..,t_D)
F6：z=x-o,t=P(z),rot_ackley(t1,..,t_m)*10^6+ackley(t_m+1,..,t_D)
F7：z=x-o,t=P(z),schwefel(t1,..,t_m)*10^6+sphere(t_m+1,..,t_D)
F8：z=x-o,t=P(z),rosenbrock(t1,..,t_m)*10^6+sphere(t_m+1,..,t_D)
F9：z=x-o,t=P(z),Σrot_elliptic(t_{(k-1)*m+1},..,t_{k*m}(k=1,..,D/2m))+elliptic(t_{D/2+1},..,t_{D})
F10：z=x-o,t=P(z),Σrot_rastrigin(t_{(k-1)*m+1},..,t_{k*m}(k=1,..,D/2m))+rastrigin(t_{D/2+1},..,t_{D})
F11：z=x-o,t=P(z),Σrot_ackley(t_{(k-1)*m+1},..,t_{k*m}(k=1,..,D/2m))+ackley(t_{D/2+1},..,t_{D})
F12：z=x-o,t=P(z),Σschwefel(t_{(k-1)*m+1},..,t_{k*m}(k=1,..,D/2m))+sphere(t_{D/2+1},..,t_{D})
F13：z=x-o,t=P(z),Σrosenbrock(t_{(k-1)*m+1},..,t_{k*m}(k=1,..,D/2m))+sphere(t_{D/2+1},..,t_{D})
F14：z=x-o,t=P(z),Σrot_elliptic(t_{(k-1)*m+1},..,t_{k*m}(k=1,..,D/m))
F15：z=x-o,t=P(z),Σrot_rastrigin(t_{(k-1)*m+1},..,t_{k*m}(k=1,..,D/m))
F16：z=x-o,t=P(z),Σrot_ackley(t_{(k-1)*m+1},..,t_{k*m}(k=1,..,D/m))
F17：z=x-o,t=P(z),Σschwefel(t_{(k-1)*m+1},..,t_{k*m}(k=1,..,D/m))
F18：z=x-o,t=P(z),Σrosenbrock(t_{(k-1)*m+1},..,t_{k*m}(k=1,..,D/m))
F19：z=x-o,schwefel(z)
F20：z=x-o,rosenbrock(z)