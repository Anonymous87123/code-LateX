# C++ 类与对象考试阴招题目化讲义

> 适合选择题、判断题、填空题、读程序输出题考前复习。  
> 本讲义的核心不是背零散结论，而是训练你看到代码后能判断：**对象何时出生、何时拷贝、何时死亡、调用的是谁的函数**。

## A. 专题：运算符重载系统讲解

### 1. 运算符重载是什么

运算符重载就是让 C++ 已有的运算符能作用在自定义类型上。它不是创造新语法，而是告诉编译器：当某个运算符遇到你的类对象时，应该调用哪个函数。

例如你写了一个复数类：

```cpp
class Complex {
public:
    int real;
    int imag;
};
```

你希望可以这样写：

```cpp
Complex c3 = c1 + c2;
```

但默认情况下，编译器不知道两个 `Complex` 应该怎么相加，所以要重载 `operator+`。

成员函数写法中：

```cpp
c1 + c2
```

大致可以理解成：

```cpp
c1.operator+(c2)
```

非成员函数写法中：

```cpp
c1 + c2
```

大致可以理解成：

```cpp
operator+(c1, c2)
```

### 2. 基本规则

选择题很爱考这些规则，先把边界记牢。

#### 不能创造新运算符

```cpp
operator**   // 错误示范：不能通过编译
operator@    // 错误示范：不能通过编译
```

只能重载 C++ 已经存在的运算符。

#### 不能改变操作数个数

`+` 本来可以是一元或二元运算符，你不能把它重载成三元运算符。后置 `++` 的 `int` 参数也只是用来区分前置和后置，不代表调用时真的传一个整数。

#### 不能改变优先级和结合性

即使重载了 `+` 和 `*`，表达式：

```cpp
a + b * c
```

仍然先算 `b * c`。运算符重载只改变“怎么算”，不改变“先算谁”。

#### 至少有一个操作数必须是自定义类型

```cpp
int operator+(int a, int b); // 错误示范：不能通过编译
```

不能改写内置类型之间的原有运算规则。

可以写：

```cpp
Complex operator+(const Complex& a, const Complex& b);
Complex operator+(const Complex& a, int b);
Complex operator+(int a, const Complex& b);
```

因为至少有一个操作数是自定义类型。

#### 这些运算符不能重载

常考不能重载：

| 运算符 | 含义 |
| --- | --- |
| `.` | 成员访问 |
| `.*` | 成员指针访问 |
| `::` | 作用域解析 |
| `?:` | 三目运算符 |
| `sizeof` | 求大小 |

记忆：**点、域、三目、大小不能重载。**

### 3. 成员函数重载和非成员函数重载

#### 成员函数写法

成员函数重载时，左操作数是当前对象，也就是 `this`，所以参数里通常只写右操作数。

```cpp
class Complex {
private:
    int real;
    int imag;

public:
    Complex(int r = 0, int i = 0) : real(r), imag(i) {}

    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }
};
```

使用：

```cpp
Complex c1(1, 2), c2(3, 4);
Complex c3 = c1 + c2;
```

可以理解成：

```cpp
Complex c3 = c1.operator+(c2);
```

#### 非成员函数写法

非成员函数没有 `this`，所以左右两个操作数都要作为参数出现。

```cpp
class Complex {
public:
    int real;
    int imag;

    Complex(int r = 0, int i = 0) : real(r), imag(i) {}
};

Complex operator+(const Complex& a, const Complex& b) {
    return Complex(a.real + b.real, a.imag + b.imag);
}
```

可以理解成：

```cpp
Complex c3 = operator+(c1, c2);
```

### 4. 哪些必须写成成员函数

这几个必须重载为成员函数：

```cpp
=
[]
()
->
```

记忆：**赋值、下标、调用、箭头，必须成员。**

```cpp
class A {
public:
    A& operator=(const A& other);
    int& operator[](int index);
    void operator()();
    A* operator->();
};
```

### 5. 输入输出为什么常写成友元非成员函数

输出运算符的常见形式是：

```cpp
cout << obj;
```

左操作数是 `cout`，类型是 `ostream`，不是你的类对象。如果把 `operator<<` 写成类的成员函数，形式会变成类似：

```cpp
obj.operator<<(cout);
```

这就不符合常用写法。因此 `<<` 和 `>>` 通常写成非成员函数；如果要访问私有成员，再声明为友元。

```cpp
#include <iostream>
using namespace std;

class Complex {
private:
    int real;
    int imag;

public:
    Complex(int r = 0, int i = 0) : real(r), imag(i) {}

    friend ostream& operator<<(ostream& out, const Complex& c);
    friend istream& operator>>(istream& in, Complex& c);
};

ostream& operator<<(ostream& out, const Complex& c) {
    out << c.real << "+" << c.imag << "i";
    return out;
}

istream& operator>>(istream& in, Complex& c) {
    in >> c.real >> c.imag;
    return in;
}
```

返回 `ostream&` 和 `istream&` 是为了支持链式操作：

```cpp
cout << c1 << c2;
cin >> c1 >> c2;
```

### 6. 传参怎么写

#### 不修改参数：用 `const` 引用

普通二元运算如果只读取右操作数，推荐写：

```cpp
Complex operator+(const Complex& other) const;
```

这里有两个 `const`：

- `const Complex& other`：不修改右操作数，并且避免拷贝。
- 函数末尾的 `const`：不修改当前对象，也就是不修改左操作数。

#### 要修改当前对象：不要写函数尾部 `const`

`+=` 会修改左操作数，所以不能写成 `const` 成员函数。

```cpp
Complex& operator+=(const Complex& other) {
    real += other.real;
    imag += other.imag;
    return *this;
}
```

#### 输入运算符的对象参数不能是 `const`

```cpp
istream& operator>>(istream& in, Complex& c) {
    in >> c.real >> c.imag;
    return in;
}
```

`Complex& c` 不能写成 `const Complex& c`，因为输入操作要修改对象。

### 7. 返回值怎么写

#### `operator+` 通常返回新对象

`c1 + c2` 不应该修改 `c1` 和 `c2`，而是产生一个新结果。

```cpp
Complex operator+(const Complex& other) const {
    return Complex(real + other.real, imag + other.imag);
}
```

不要返回局部对象引用：

```cpp
Complex& operator+(const Complex& other) {
    Complex temp(real + other.real, imag + other.imag);
    return temp; // 错误示范：不能返回局部变量引用
}
```

记忆：**加减乘除造新对象，通常返回值。**

#### `operator+=` 通常返回当前对象引用

```cpp
Complex& operator+=(const Complex& other) {
    real += other.real;
    imag += other.imag;
    return *this;
}
```

这样可以支持：

```cpp
c1 += c2 += c3;
```

记忆：**复合赋值改自己，返回 `*this` 引用。**

#### `operator=` 通常返回引用

```cpp
class A {
public:
    A& operator=(const A& other) {
        if (this != &other) {
            // 复制数据
        }
        return *this;
    }
};
```

返回 `A&` 是为了支持连等：

```cpp
a = b = c;
```

如果类中管理动态资源，赋值运算符还要特别注意自赋值、释放旧资源、深拷贝等问题。

#### `operator[]` 通常返回引用

```cpp
class Array {
private:
    int data[10];

public:
    int& operator[](int index) {
        return data[index];
    }

    const int& operator[](int index) const {
        return data[index];
    }
};
```

返回引用是为了支持：

```cpp
arr[0] = 100;
```

如果返回 `int`，得到的是副本，不能修改原数组元素。

### 8. 常见运算符写法

#### `+` 和 `+=`

```cpp
class Complex {
private:
    int real;
    int imag;

public:
    Complex(int r = 0, int i = 0) : real(r), imag(i) {}

    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }

    Complex& operator+=(const Complex& other) {
        real += other.real;
        imag += other.imag;
        return *this;
    }
};
```

记忆：

```text
+  不改自己，返回新对象
+= 改自己，返回自己引用
```

#### 前置 `++` 和后置 `++`

```cpp
class Counter {
private:
    int value;

public:
    Counter(int v = 0) : value(v) {}

    Counter& operator++() {
        ++value;
        return *this;
    }

    Counter operator++(int) {
        Counter old = *this;
        value++;
        return old;
    }
};
```

前置 `++a`：先加，再返回自己，所以返回引用。  
后置 `a++`：先返回旧值，再加，所以要保存旧对象，返回值。

记忆：**前置无参返引用，后置 `int` 返旧值。**

#### 比较运算符

比较通常返回 `bool`。

```cpp
bool operator==(const Complex& other) const {
    return real == other.real && imag == other.imag;
}

bool operator!=(const Complex& other) const {
    return !(*this == other);
}
```

如果需要排序，常重载 `<`：

```cpp
class Student {
private:
    int score;

public:
    Student(int s) : score(s) {}

    bool operator<(const Student& other) const {
        return score < other.score;
    }
};
```

#### 函数调用运算符 `()`

让对象像函数一样调用。

```cpp
class Adder {
public:
    int operator()(int a, int b) const {
        return a + b;
    }
};

int main() {
    Adder add;
    cout << add(3, 4) << endl;
}
```

这种对象常叫函数对象。

#### 箭头运算符 `->`

常用于智能指针类。

```cpp
class Student {
public:
    void show() {}
};

class Ptr {
private:
    Student* p;

public:
    Ptr(Student* ptr) : p(ptr) {}

    Student* operator->() {
        return p;
    }
};
```

### 9. 常见错误

#### `operator+` 返回引用

```cpp
Complex& operator+(const Complex& other) {
    Complex temp(real + other.real, imag + other.imag);
    return temp; // 错误示范：不能返回局部变量引用
}
```

`temp` 是局部对象，函数结束就销毁，所以不能返回它的引用。

#### `operator+=` 返回 `void`

```cpp
void operator+=(const Complex& other);
```

这不是语法错误，但不推荐。它能支持 `a += b`，但不能自然支持链式表达式 `a += b += c`。考试中更标准的写法是：

```cpp
Complex& operator+=(const Complex& other);
```

#### 后置 `++` 返回引用

后置 `a++` 要返回旧值，而旧值通常保存在局部对象中，所以不能返回引用。标准思路是返回值：

```cpp
Counter operator++(int);
```

### 10. 类型转换函数

类型转换函数也是一种特殊的运算符重载。它的作用是：让类对象可以转换成某个目标类型。

标准写法：

```cpp
class Xclass {
public:
    operator Type() {
        return Type_Value;
    }
};
```

类外定义写法：

```cpp
Xclass::operator Type() {
    return Type_Value;
}
```

注意它有三个“没有/不能”：

```text
1. 没有返回值类型，不能写 Type Xclass::operator Type()。
2. 没有参数，不能写 operator Type(int x)。
3. 必须是成员函数，不能写成 friend 非成员函数。
```

例子：

```cpp
#include <iostream>
using namespace std;

class Number {
private:
    int value;

public:
    Number(int v) : value(v) {}

    operator int() const {
        return value;
    }
};

int main() {
    Number n(10);
    int x = n;  // 等价于 int x = n.operator int();

    cout << x << endl;
    return 0;
}
```

输出：

```text
10
```

典型选择题：

```cpp
// 假设 Xclass 是类名，Type 是目标类型，Type_Value 是 Type 类型表达式。
```

正确形式是：

```cpp
Xclass::operator Type() {
    return Type_Value;
}
```

错误示范：

```cpp
Xclass::operator Type(Type t) { return Type_Value; }
// 错：类型转换函数不能有参数

friend Xclass::operator Type() { return Type_Value; }
// 错：类型转换函数必须是成员函数，不能是 friend 非成员函数

Type Xclass::operator Type() { return Type_Value; }
// 错：类型转换函数不能写返回值类型
```

记忆：

```text
转换函数像施法：operator 目标类型()。
不写返回值，不带参数，只能成员。
```

### 11. 考试常见结论

1. 运算符重载不能创造新运算符。
2. 运算符重载不能改变优先级。
3. 运算符重载不能改变结合性。
4. 运算符重载不能改变操作数个数。
5. 运算符重载至少有一个操作数是自定义类型。
6. `.`, `.*`, `::`, `?:`, `sizeof` 不能重载。
7. `=`, `[]`, `()`, `->` 必须重载为成员函数。
8. `<<`, `>>` 通常重载为友元非成员函数。
9. `operator+` 通常返回新对象。
10. `operator+=` 通常返回当前对象引用。
11. 前置 `++` 无参数，后置 `++` 有一个 `int` 参数。
12. 前置 `++` 返回引用，后置 `++` 返回旧值。
13. `operator[]` 通常返回引用。
14. 比较运算符通常返回 `bool`。
15. 类型转换函数写法是 `operator 类型()`，没有返回类型。

### 12. 记忆总表

| 运算符 | 推荐形式 | 返回值 | 记忆 |
| --- | --- | --- | --- |
| `+` | 成员/非成员 | 新对象 | 加法造新 |
| `-` | 成员/非成员 | 新对象 | 减法造新 |
| `*` | 成员/非成员 | 新对象 | 乘法造新 |
| `/` | 成员/非成员 | 新对象 | 除法造新 |
| `+=` | 成员 | `T&` | 改自己，返自己 |
| `-=` | 成员 | `T&` | 改自己，返自己 |
| `=` | 必须成员 | `T&` | 支持连等 |
| `==` | 成员/非成员 | `bool` | 比较真假 |
| `<` | 成员/非成员 | `bool` | 排序常用 |
| `[]` | 必须成员 | 元素引用 | 支持 `arr[i] = x` |
| `()` | 必须成员 | 看需求 | 对象当函数 |
| `->` | 必须成员 | 指针/代理 | 智能指针 |
| `<<` | 友元非成员 | `ostream&` | 支持链式输出 |
| `>>` | 友元非成员 | `istream&` | 支持链式输入 |
| 前置 `++` | 成员 | `T&` | 先加后用 |
| 后置 `++` | 成员 | `T` | 先用后加 |

一句话总口诀：

```text
普通四则造新值，复合赋值返自身；
输入输出返流，比较返回 bool；
前置 ++ 返引用，后置 ++ 返旧值；
赋值下标调用箭头，必须写成成员函数。
```

## B. 专题：输入输出流与文件操作

### 1. 先建立整体地图

流可以理解成“数据流动的管道”。从键盘到程序、从程序到屏幕、从文件到程序、从程序到文件，本质都是数据通过流对象传递。

考试里最常见的是四类：

| 类型/对象 | 作用 | 头文件 |
| --- | --- | --- |
| `cin` | 标准输入，通常从键盘读 | `<iostream>` |
| `cout` | 标准输出，通常向屏幕写 | `<iostream>` |
| `ifstream` | input file stream，从文件读 | `<fstream>` |
| `ofstream` | output file stream，向文件写 | `<fstream>` |
| `fstream` | file stream，可读可写文件 | `<fstream>` |
| `istringstream` | 从字符串中读 | `<sstream>` |
| `ostringstream` | 向字符串中写 | `<sstream>` |
| `setw` / `setfill` / `setprecision` | 格式控制 | `<iomanip>` |

记忆：

```text
i = input = 输入 = 读
o = output = 输出 = 写
f = file = 文件
stringstream = 字符串流
```

所以：

```cpp
ifstream fin;   // 文件输入流，读文件
ofstream fout;  // 文件输出流，写文件
fstream file;   // 文件输入输出流，可读可写
```

### 2. 控制台输入输出：`cin` / `cout`

```cpp
#include <iostream>
using namespace std;

int main() {
    int a;
    double x;

    cin >> a >> x;
    cout << "a=" << a << ", x=" << x << endl;

    return 0;
}
```

如果输入：

```text
20 50.5
```

输出：

```text
a=20, x=50.5
```

`>>` 叫提取运算符，它读取时会自动跳过空白字符，读 `string` 时遇到空格、换行、Tab 就停止。

```cpp
string s;
cin >> s;
```

如果输入：

```text
This is a test
```

`s` 只得到：

```text
This
```

如果要读整行，用：

```cpp
getline(cin, s);
```

### 3. 文件写入：`ofstream`

写文件用 `ofstream`。

```cpp
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    ofstream fout("test.txt");

    fout << "Data: " << 20 << " " << 50.5;

    fout.close();
    return 0;
}
```

运行后，`test.txt` 文件内容是：

```text
Data: 20 50.5
```

`ofstream fout("test.txt");` 默认以输出方式打开文件。如果文件不存在，会创建；如果文件已存在，通常会清空原内容再写。

### 4. 文件读取：`ifstream`

假设 `test.txt` 内容是：

```text
Data: 20 50.5
```

代码：

```cpp
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ifstream fin("test.txt");

    string s;
    int a;
    double x;

    fin >> s >> a >> x;

    cout << "string=" << s << ", a=" << a << ", x=" << x;

    fin.close();
    return 0;
}
```

输出：

```text
string=Data:, a=20, x=50.5
```

解析：`>>` 按空白分隔，所以 `"Data:"` 被读入字符串 `s`，`20` 被读入 `a`，`50.5` 被读入 `x`。

### 5. 打开文件后先判断是否成功

```cpp
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    ifstream fin("data.txt");

    if (!fin) {
        cout << "文件打开失败" << endl;
        return 1;
    }

    int x;
    fin >> x;
    cout << x << endl;

    fin.close();
    return 0;
}
```

也可以写：

```cpp
if (!fin.is_open()) {
    cout << "文件打开失败" << endl;
}
```

考试记忆：**打开文件后，先判断是否成功。**

### 6. 三种文件流对比

| 类型 | 用途 | 常用打开方式 |
| --- | --- | --- |
| `ifstream` | 读文件 | `ios::in` |
| `ofstream` | 写文件 | `ios::out` |
| `fstream` | 读写文件 | `ios::in | ios::out` |

```cpp
ifstream fin("a.txt", ios::in);
ofstream fout("b.txt", ios::out);
fstream file("c.txt", ios::in | ios::out);
```

基础考试里可以这么记：

```text
ifstream 读文件
ofstream 写文件
fstream 可读可写
```

### 7. 文件打开方式 `ios::xxx`

| 打开方式 | 含义 |
| --- | --- |
| `ios::in` | 读 |
| `ios::out` | 写 |
| `ios::app` | 追加写，写到文件末尾 |
| `ios::ate` | 打开后定位到文件末尾，但之后可以移动 |
| `ios::trunc` | 打开时清空原文件 |
| `ios::binary` | 二进制方式打开 |

#### `ios::out`

```cpp
ofstream fout("data.txt", ios::out);
```

写文件。如果文件已有内容，通常会清空。

#### `ios::app`

```cpp
ofstream fout("data.txt", ios::app);
```

追加写，不清空原文件，新内容写到末尾。

如果原文件是：

```text
ABC
```

执行：

```cpp
ofstream fout("data.txt", ios::app);
fout << "DEF";
```

文件变成：

```text
ABCDEF
```

#### `ios::binary`

二进制读写时使用：

```cpp
ofstream fout("data.dat", ios::out | ios::binary);
ifstream fin("data.dat", ios::in | ios::binary);
```

### 8. `open()` 函数打开文件

文件流有两种常见打开方式。

第一种：定义对象时直接打开。

```cpp
ifstream fin("student.txt", ios::in);
ofstream fout("result.txt", ios::out);
fstream file("data.txt", ios::in | ios::out);
```

第二种：先定义流对象，再调用 `open()`。

```cpp
ifstream fin;
fin.open("student.txt", ios::in);

ofstream fout;
fout.open("result.txt", ios::out);

fstream file;
file.open("data.txt", ios::in | ios::out);
```

这两种写法本质一样。考试看到：

```cpp
流对象.open("文件名", 打开方式);
```

就按“用某种模式打开某个文件”来理解。

常见搭配：

| 写法 | 含义 |
| --- | --- |
| `ifstream fin("a.txt");` | 默认读文件 |
| `ifstream fin("a.txt", ios::in);` | 明确以读方式打开 |
| `ofstream fout("a.txt");` | 默认写文件，通常会清空原内容 |
| `ofstream fout("a.txt", ios::out);` | 明确以写方式打开 |
| `ofstream fout("a.txt", ios::out | ios::app);` | 追加写 |
| `ofstream fout("a.dat", ios::out | ios::binary);` | 二进制写 |
| `ifstream fin("a.dat", ios::in | ios::binary);` | 二进制读 |
| `fstream file("a.txt", ios::in | ios::out);` | 同时读写 |
| `fstream file("a.txt", ios::in | ios::out | ios::ate);` | 同时读写，打开后定位到末尾 |

注意：`ios::binary` 和 `ios::ate` 通常只是“附加属性”，一般要和 `ios::in` 或 `ios::out` 搭配使用。

#### 典型题：判断打开文件语句哪一个错误

题目：下列打开文件的语句中，哪一个是错误的？

```cpp
A. ofstream ofile; ofile.open("student.txt", ios::binary);
B. ifstream ifile("student.txt", ios::out);
C. fstream iofile; iofile.open("student.txt", ios::ate);
D. ifstream ifile("student.txt", ios::in);
```

按更严格的标准库口径，最应判错的是 **C**。

解析：

```text
A：ofstream 的 open 会带输出语义，ios::binary 表示二进制方式。更规范写法是 ios::out | ios::binary。
B：很多教材会说 ifstream 应该读文件，不该配 ios::out；但标准库的 ifstream 会自动补 ios::in，因此实际可能按 ios::in | ios::out 打开。
C：fstream 需要明确读/写方向。ios::ate 只是“打开后定位到末尾”，不是读或写方向。更规范应写 ios::in | ios::out | ios::ate。
D：ifstream 以 ios::in 打开，正确。
```

如果按基础教材的简化口径，可能把 **B** 也视为错误，因为：

```text
ifstream 对应 ios::in
ofstream 对应 ios::out
fstream 对应 ios::in | ios::out
```

所以遇到这种题要看老师/教材口径。为了考试稳妥，建议这样写：

```cpp
ofstream ofile;
ofile.open("student.txt", ios::out | ios::binary);

ifstream ifile;
ifile.open("student.txt", ios::in);

fstream iofile;
iofile.open("student.txt", ios::in | ios::out | ios::ate);
```

记忆：

```text
open 两参数：文件名 + 打开方式。
binary/ate 是附加状态，读写方向还得靠 in/out。
考试简化：ifstream 配 in，ofstream 配 out，fstream 配 in|out。
```

### 9. 文本文件 vs 二进制文件

文本文件是人能直接看懂的内容：

```text
20 50.5 Hello
```

常用：

```cpp
fout << a << " " << x;
fin >> a >> x;
```

二进制文件按内存字节保存，人直接打开通常看不懂，常用：

```cpp
write()
read()
```

写入一个 `double`：

```cpp
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    double number = 3.14;

    ofstream fout("num.dat", ios::out | ios::binary);
    fout.write((char*)&number, sizeof(double));
    fout.close();

    return 0;
}
```

读取：

```cpp
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    double number;

    ifstream fin("num.dat", ios::in | ios::binary);
    fin.read((char*)&number, sizeof(double));

    cout << number << endl;

    fin.close();
    return 0;
}
```

重点：

```cpp
fout.write((char*)&number, sizeof(double));
fin.read((char*)&number, sizeof(double));
```

`write` 和 `read` 的第一个参数要求是 `char*` 类型，所以考试题常出现强制转换：

```cpp
(char*)&number
```

更现代的写法是：

```cpp
reinterpret_cast<char*>(&number)
```

### 10. 二进制读写结构体

```cpp
#include <iostream>
#include <fstream>
using namespace std;

struct Student {
    int number;
    char name[20];
    double score;
};

int main() {
    Student s = {1, "Tom", 95.5};

    ofstream fout("student.dat", ios::out | ios::binary);
    fout.write((char*)&s, sizeof(Student));
    fout.close();

    return 0;
}
```

读取：

```cpp
Student s;

ifstream fin("student.dat", ios::in | ios::binary);
fin.read((char*)&s, sizeof(Student));

cout << s.number << " " << s.name << " " << s.score << endl;
```

填空题常填：

```cpp
fout.write((char*)&s, sizeof(Student));
fin.read((char*)&s, sizeof(Student));
```

#### 选择题秒杀：文本文件和二进制文件

题目：关于文件操作的描述，正确的是哪一个？

```text
A. 文本文件的读写速度比二进制文件快。
B. 二进制文件的读写操作不需要进行格式转换。
C. 二进制文件不适合存储大量数据。
D. 文本文件和二进制文件的存储格式相同。
```

答案：**B**

解析：

- A 错。一般情况下，二进制文件直接按内存字节读写，不需要把数字转成字符文本，也不需要从字符文本再转回数字，所以读写效率通常更高。
- B 对。二进制读写使用 `read` / `write`，按字节保存和恢复数据，通常不需要文本格式转换。
- C 错。二进制文件很适合保存大量数据，例如结构体数组、图像、音频、数据库底层数据等。
- D 错。文本文件保存的是字符形式，二进制文件保存的是内存字节形式，存储格式不同。

记忆：

```text
文本文件：人好看，机器要转换。
二进制文件：人难看，机器读写快，适合大量数据。
```

### 11. 先写文件再读文件

```cpp
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ofstream fout("test.txt");
    fout << "Data: " << 20 << " " << 50.5;
    fout.close();

    ifstream fin("test.txt");

    string s;
    int a;
    double x;

    fin >> s >> a >> x;

    cout << "string=" << s
         << ", a=" << a
         << ", x=" << x;

    fin.close();
    return 0;
}
```

文件内容：

```text
Data: 20 50.5
```

屏幕输出：

```text
string=Data:, a=20, x=50.5
```

关键点：

```text
先以 out 方式写入，关闭后，再以 in 方式读取。
```

如果先写同一个文件再读，建议一定先 `fout.close()`。

### 12. `getline` / `get` / `width` 输入函数族

```cpp
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ifstream fin("data.txt");

    string line;
    getline(fin, line);

    cout << line << endl;

    fin.close();
    return 0;
}
```

如果文件内容是：

```text
This is a test
```

输出：

```text
This is a test
```

`getline` 有两大类写法，考试很喜欢混着考。

| 写法 | 类型 | 读到哪里 | 适合对象 |
| --- | --- | --- | --- |
| `getline(cin, line)` | 非成员函数 | 默认读到换行 | `string line` |
| `getline(fin, line)` | 非成员函数 | 默认读到换行 | `string line` |
| `getline(cin, line, '#')` | 非成员函数 | 读到指定分隔符 `#` | `string line` |
| `fin.getline(buf, 100)` | 流成员函数 | 默认读到换行 | `char buf[100]` |
| `fin.getline(buf, 100, '#')` | 流成员函数 | 读到指定分隔符 `#` | `char buf[100]` |

一句话：

```text
读 string：getline(流, string变量)
读 char数组：流.getline(char数组, 最大长度)
```

#### `getline` 读 `string`

```cpp
string line;
getline(cin, line);
getline(fin, line);
getline(fin, line, '#');
```

第三个参数是分隔符：

```cpp
getline(fin, line, '#');
```

表示一直读到 `#` 为止，`#` 本身被取走但不放进 `line`。

#### `getline` 读字符数组

```cpp
char buf[100];
cin.getline(buf, 100);
fin.getline(buf, 100);
fin.getline(buf, 100, '#');
```

这里的 `100` 表示缓冲区大小。最多存放 99 个普通字符，最后一个位置留给 `'\0'`。

#### `get()` 常见写法

`get` 是“按字符/字符数组读”的成员函数，比 `>>` 更细。

| 写法 | 含义 | 是否跳过空白 |
| --- | --- | --- |
| `ch = cin.get()` | 读取一个字符并返回 | 不跳过 |
| `cin.get(ch)` | 读取一个字符放入 `ch` | 不跳过 |
| `cin.get(buf, 100)` | 读一串字符到数组，遇换行停 | 不跳过 |
| `cin.get(buf, 100, '#')` | 读到指定分隔符 `#` 停 | 不跳过 |

和 `>>` 对比：

```cpp
char ch;
cin >> ch;    // 跳过空格、换行，读一个非空白字符
cin.get(ch);  // 不跳过空白，空格和换行也能读到
```

`get(buf, n)` 和 `getline(buf, n)` 的常考区别：

```text
getline 读到换行后，会把换行符取走。
get 读到换行前停止，通常把换行符留在输入流里。
```

#### `cin.width(n)` 输入宽度

`width(n)` 不只是 `cout` 能用，`cin` 也能用：

```cpp
char name[10];
cin.width(5);
cin >> name;
```

对字符数组来说，`cin.width(5)` 表示下一次读入最多占用 5 个位置，其中要留一个给 `'\0'`，所以最多读 4 个普通字符。

如果输入：

```text
abcdef
```

执行：

```cpp
char s[10];
cin.width(5);
cin >> s;
```

则 `s` 得到：

```text
abcd
```

剩下的 `ef` 仍留在输入流中，可能影响下一次读取。

对 `string` 来说，`width(n)` 也会限制下一次格式化读取的大致最大字段宽度；基础考试最常见还是考字符数组。

记忆：

```text
cout.width(n)：控制下一次输出最小宽度，短了补，长了不截断。
cin.width(n)：控制下一次输入最大宽度，常用于 char 数组防止越界。
width 只管下一次，之后失效。
```

#### `>>` 和 `getline` 混用陷阱

```cpp
int age;
string name;

cin >> age;
getline(cin, name);
```

`getline` 可能读到上一行剩下的换行符，导致 `name` 是空字符串。

常见处理：

```cpp
cin >> age;
cin.ignore();
getline(cin, name);
```

考试记忆：**`cin >>` 后面接 `getline`，常常要 `cin.ignore()`。**

### 13. 字符串流 `stringstream`

头文件：

```cpp
#include <sstream>
```

#### `istringstream`：从字符串读

```cpp
#include <iostream>
#include <sstream>
#include <string>
using namespace std;

int main() {
    string str = "This is a test";
    string s1, s2, s3, s4;

    istringstream input(str);

    input >> s1 >> s2 >> s3 >> s4;

    cout << s1 << endl;
    return 0;
}
```

输出：

```text
This
```

因为 `>>` 按空格分隔，所以：

```text
s1 = "This"
s2 = "is"
s3 = "a"
s4 = "test"
```

#### `ostringstream`：向字符串写

```cpp
#include <iostream>
#include <sstream>
#include <string>
using namespace std;

int main() {
    ostringstream output;

    output << "score=" << 95;

    string s = output.str();
    cout << s << endl;

    return 0;
}
```

输出：

```text
score=95
```

### 14. 格式控制头文件 `<iomanip>`

常用格式控制：

| 函数/控制符 | 作用 |
| --- | --- |
| `setw(n)` | 设置下一个输出项宽度 |
| `setfill(c)` | 设置填充字符 |
| `left` | 左对齐 |
| `right` | 右对齐 |
| `setprecision(n)` | 设置精度 |
| `fixed` | 固定小数位 |
| `dec` | 十进制 |
| `hex` | 十六进制 |
| `oct` | 八进制 |
| `setiosflags(...)` | 设置格式标志 |
| `resetiosflags(...)` | 清除格式标志 |

使用 `setw`、`setfill`、`setprecision` 时要包含：

```cpp
#include <iomanip>
```

### 15. 进制控制：`dec` / `hex` / `oct`

```cpp
#include <iostream>
using namespace std;

int main() {
    int num1 = 20;
    int num2 = 30;

    cout << "十进制: " << dec << num1 << endl;
    cout << "十六进制: " << hex << num1 << " " << num2 << endl;
    cout << "八进制: " << oct << num1 << endl;

    return 0;
}
```

输出：

```text
十进制: 20
十六进制: 14 1e
八进制: 24
```

`20` 的十六进制是 `14`，`30` 的十六进制是 `1e`，`20` 的八进制是 `24`。

注意：`hex`、`oct`、`dec` 会影响后面整数的输出，直到再次改变。

### 16. `setw(n)`：宽度控制

`setw(n)` 设置下一个输出项的最小宽度。

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    cout << setw(5) << "A" << "B" << endl;
    cout << setw(5) << "A" << setw(5) << "B" << endl;
    return 0;
}
```

输出可理解为：

```text
    AB
    A    B
```

超级重点：

```text
setw(n) 只影响紧随其后的一个输出项。
```

### 17. `setfill(c)`：填充字符

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    cout << setfill('+') << setw(10) << "Data" << endl;
    return 0;
}
```

默认右对齐，所以输出：

```text
+++++Data
```

`"Data"` 长度是 4，宽度是 10，需要补 6 个 `+`。

注意：`setfill` 会持续生效，直到再次修改填充字符。

### 18. `left` / `right`：左右对齐

默认右对齐。

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    cout << setw(5) << "A" << "B" << endl;
    cout << left << setw(5) << "A" << "B" << endl;
    return 0;
}
```

输出可理解为：

```text
    AB
A    B
```

第一行：`A` 占 5 个宽度，默认右对齐，前面补 4 个空格，然后接 `B`。

第二行：`A` 左对齐，后面补 4 个空格，然后接 `B`。

注意：

```text
left/right 会持续生效，setw 只生效一次。
```

### 19. `setprecision(n)` 精度控制

这是格式控制里最大的坑。

#### 不配合 `fixed`

默认情况下，`setprecision(n)` 表示 **有效数字总位数**。

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double pi = 3.1415926535;

    cout << pi << endl;
    cout << setprecision(8) << pi << endl;

    return 0;
}
```

输出大致：

```text
3.14159
3.1415927
```

#### 配合 `fixed`

`fixed << setprecision(n)` 表示 **保留 n 位小数**。

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double pi = 3.1415926535;

    cout << fixed << setprecision(4) << pi << endl;
    cout << pi << endl;

    return 0;
}
```

输出：

```text
3.1416
3.1416
```

第二行仍然是 4 位小数，因为 `fixed` 和 `setprecision(4)` 会持续生效。

记忆：

```text
setprecision 单独用：有效数字
fixed + setprecision：小数位数
```

### 20. `setiosflags`

`setiosflags` 是老式格式控制，也常考。

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    cout << setfill('+')
         << setw(10)
         << setiosflags(ios::right)
         << "Data"
         << endl;
    return 0;
}
```

输出：

```text
+++++Data
```

常见写法：

| 写法 | 含义 |
| --- | --- |
| `setiosflags(ios::left)` | 左对齐 |
| `setiosflags(ios::right)` | 右对齐 |
| `setiosflags(ios::fixed)` | 固定小数位 |
| `setiosflags(ios::showpoint)` | 强制显示小数点 |
| `setiosflags(ios::showpos)` | 正数显示 `+` |

取消标志：

```cpp
cout << resetiosflags(ios::left);
```

### 21. `cout.width()` 和 `cout.setf()`

除了 `<iomanip>` 里的 `setw`、`setprecision`、`setiosflags`，考试还会考输出流对象自己的成员函数：

```cpp
cout.width(n);
cout.setf(标志);
cout.setf(标志, 标志组);
```

先记住最重要的区别：

```text
cout.width(n) 只影响下一次输出，效果类似 setw(n)。
cout.setf(...) 设置格式状态，通常会持续影响后续输出。
```

常见标志：

| 标志 | 含义 |
| --- | --- |
| `ios::left` | 左对齐 |
| `ios::right` | 右对齐 |
| `ios::showpos` | 正数前显示 `+` |
| `ios::scientific` | 科学计数法 |
| `ios::fixed` | 固定小数形式 |
| `ios::dec` | 十进制整数 |
| `ios::hex` | 十六进制整数 |
| `ios::oct` | 八进制整数 |

常见标志组：

| 标志组 | 管什么 |
| --- | --- |
| `ios::basefield` | 整数进制：`dec` / `hex` / `oct` |
| `ios::adjustfield` | 对齐方式：`left` / `right` / `internal` |
| `ios::floatfield` | 浮点格式：`fixed` / `scientific` |

两参数 `setf` 的意思是：先清除某一组旧标志，再设置新标志。

```cpp
cout.setf(ios::dec, ios::basefield);       // 在进制组里设置十进制
cout.setf(ios::right, ios::adjustfield);   // 在对齐组里设置右对齐
cout.setf(ios::scientific, ios::floatfield); // 在浮点组里设置科学计数法
```

有些老题会写成：

```cpp
cout.setf(ios::right, ios::left);
```

这表示“清掉 `left`，设置 `right`”。更规范、更好记的写法是：

```cpp
cout.setf(ios::right, ios::adjustfield);
```

#### 典型题：`width`、`setf` 和持续状态

题目：写出下面程序的输出。为看清空格，解析中用 `·` 表示空格。

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double x = 123.456;

    cout.width(10);
    cout.setf(ios::dec, ios::basefield);
    cout << x << endl;

    cout.setf(ios::left);
    cout << x << endl;

    cout.width(15);
    cout.setf(ios::right, ios::left);
    cout << x << endl;

    cout.setf(ios::showpos);
    cout << x << endl;

    cout.setf(ios::scientific);
    cout << x << endl;

    return 0;
}
```

答案：

```text
   123.456
123.456
        123.456
+123.456
+1.234560e+02
```

用 `·` 表示空格：

```text
···123.456
123.456
········123.456
+123.456
+1.234560e+02
```

逐行解析：

```text
double x = 123.456;
默认精度是 6 位有效数字，123.456 正好按 123.456 输出。

cout.width(10);
只影响下一次输出。123.456 长度为 7，宽度 10，默认右对齐，所以前面补 3 个空格。

cout.setf(ios::dec, ios::basefield);
设置整数进制为十进制。这里输出的是 double，所以基本看不出影响。

cout.setf(ios::left);
设置左对齐，但下一句没有设置宽度，所以看不出对齐效果，仍输出 123.456。

cout.width(15);
下一次输出宽度为 15。

cout.setf(ios::right, ios::left);
清掉 left，设置 right。123.456 长度为 7，宽度 15，所以前面补 8 个空格。

cout.setf(ios::showpos);
正数前显示 +，所以输出 +123.456。这个状态会持续。

cout.setf(ios::scientific);
改成科学计数法。showpos 仍然有效，所以输出 +1.234560e+02。
```

坑点：

```text
width 只管下一次输出，用完就失效。
left/right/showpos/scientific 这类格式标志会持续。
dec/hex/oct 主要影响整数，不影响 double 的普通输出。
scientific 默认配合默认精度 6，表示小数点后 6 位。
showpos 一旦设置，后面的正数都会带 +，除非取消。
```

记忆：

```text
width 像一次性门票，只管下一个。
setf 像开关，打开后会持续。
basefield 管进制，adjustfield 管对齐，floatfield 管浮点。
```

### 22. 文件指针定位：`seekg` / `seekp` / `tellg` / `tellp`

先记字母：

```text
g = get = 读
p = put = 写
```

| 函数 | 含义 |
| --- | --- |
| `seekg` | 移动读指针 |
| `tellg` | 获取读指针位置 |
| `seekp` | 移动写指针 |
| `tellp` | 获取写指针位置 |

位置基准：

| 写法 | 含义 |
| --- | --- |
| `ios::beg` | 文件开头 |
| `ios::cur` | 当前位置 |
| `ios::end` | 文件末尾 |

例子：

```cpp
fin.seekg(10, ios::beg);  // 从文件开头向后 10 个字节
fin.seekg(0, ios::end);   // 移到文件末尾
fin.seekg(-5, ios::cur);  // 从当前位置向前 5 个字节
```

### 23. `seekg` / `tellg` 求文件大小

```cpp
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    ifstream fin("data.txt");

    fin.seekg(0, ios::end);

    streampos pos = fin.tellg();

    cout << "文件大小=" << pos << endl;

    fin.close();
    return 0;
}
```

`fin.seekg(0, ios::end);` 把读指针移动到文件末尾。  
`fin.tellg();` 返回当前读指针位置，也就是文件大小。

### 24. 读文件循环

推荐写法：

```cpp
int x;

while (fin >> x) {
    cout << x << endl;
}
```

不推荐优先写：

```cpp
while (!fin.eof()) {
    fin >> x;
    cout << x << endl;
}
```

因为这种写法容易多读一次或输出旧数据。

记忆：

```text
读文件循环：while (fin >> x)
不要迷信 while (!fin.eof())
```

### 25. 文件读写真题型：最大、最小、平均值

假设文件 `students.txt` 内容：

```text
90
80
100
```

代码：

```cpp
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    ifstream fin("students.txt");

    int score;
    int maxScore = 0;
    int minScore = 100;
    int total = 0;
    int n = 0;

    while (fin >> score) {
        if (score > maxScore) maxScore = score;
        if (score < minScore) minScore = score;

        total += score;
        n++;
    }

    cout << "max=" << maxScore << endl;
    cout << "min=" << minScore << endl;
    cout << "average=" << (double)total / n << endl;

    fin.close();
    return 0;
}
```

输出：

```text
max=100
min=80
average=90
```

考试常填：

```cpp
ifstream fin("students.txt");
while (fin >> score)
(double)total / n
```

### 26. 文件同时读写：`fstream`

```cpp
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    fstream file("data.txt", ios::in | ios::out);

    if (!file) {
        cout << "open failed" << endl;
        return 1;
    }

    int x;
    file >> x;

    file.seekp(0, ios::end);
    file << " " << 100;

    file.close();
    return 0;
}
```

基础考试一般只要求知道：

```cpp
fstream file("data.txt", ios::in | ios::out);
```

表示读写打开。读写混用时，经常需要 `seekg` / `seekp` 调整位置。

#### `fstream` 填空题救命表

`fstream` 在填空题里经常不是单独考“可读可写”，而是和文本文件、二进制文件、结构体、文件头、结束标志揉在一起考。遇到这类题，先按下面顺序扫描：

```text
1. 有没有 #include <fstream>
2. 是读文本还是写文本：ios::in / ios::out
3. 是二进制文件吗：要不要加 ios::binary
4. 是结构体整块读写吗：write/read + (char*)&对象 + sizeof(类型)
5. 是否先用 getline 跳过表头
6. 最后是否 close 输入流和输出流
```

常见填空：

| 题目意图 | 常填内容 |
| --- | --- |
| 使用文件流 | `#include <fstream>` |
| 打开输入文件 | `ios::in` |
| 打开输出文件 | `ios::out` |
| 打开二进制输出文件 | `ios::out | ios::binary` |
| 打开二进制输入文件 | `ios::in | ios::binary` |
| 读一行表头 | `in.getline(buffer, 100);` |
| 文本格式读字段 | `in >> emp.id >> emp.name >> emp.department >> emp.salary` |
| 二进制写结构体 | `out.write((char*)&emp, sizeof(Employee));` |
| 二进制读结构体 | `in.read((char*)&emp, sizeof(Employee));` |
| 关闭输入文件 | `in.close();` |
| 关闭输出文件 | `out.close();` |

注意：文件名里的反斜杠要写成双反斜杠，例如：

```cpp
fstream in("d:\\employees.txt", ios::in);
fstream out("d:\\employees.dat", ios::out | ios::binary);
```

如果试卷图片看起来像 `d:\employees.txt`，实际 C++ 字符串中规范写法仍应是 `d:\\employees.txt`，或者写成原始字符串：

```cpp
fstream in(R"(d:\employees.txt)", ios::in);
```

#### 典型题：文本员工信息转二进制结构体文件

题目：补全下面程序。程序从文本文件读取员工信息，写入二进制文件，并写入一个默认员工作为文件结束标志。

```cpp
#include <iostream>
// (11)
using namespace std;

struct Employee {
    int id;               // 员工编号
    char name[30];        // 员工姓名
    char department[20];  // 部门名称
    float salary;         // 工资
};

const Employee defaultEmployee = {0, "noName", "noDepartment", 0.0};

int main() {
    char buffer[100];
    Employee emp;

    fstream in("d:\\employees.txt",  (12)  );  // 打开输入文件的模式
    fstream out("d:\\employees.dat", (13)  );  // 打开输出文件的模式

    if (!in || !out) {
        cerr << "File could not be opened!" << endl;
        abort();
    }

    // 读取文件头信息
    in.getline(buffer, 100);
    in.getline(buffer, 100);

    // 读取员工信息并写入二进制文件
    while (in >> emp.id >> emp.name >> emp.department >> emp.salary) {
        cout << emp.id << '\t' << emp.name << '\t'
             << emp.department << '\t' << emp.salary << endl;

        out.write((char*)&emp, sizeof(Employee));
    }

    (14);  // 写入默认员工信息作为文件结束标志
    (15);
    out.close();

    return 0;
}
```

答案：

```cpp
(11) #include <fstream>
(12) ios::in
(13) ios::out | ios::binary
(14) out.write((char*)&defaultEmployee, sizeof(Employee))
(15) in.close()
```

补充：严格按标准写完整程序时，`abort()` 来自 `<cstdlib>`，所以真实工程里还应包含 `#include <cstdlib>`。但本题 `(11)` 位于文件流代码前，主要考点是 `fstream` 所需的 `#include <fstream>`。

逐行解析：

```text
#include <fstream>
只要出现 ifstream、ofstream、fstream，就要包含 <fstream>。

fstream in("d:\\employees.txt", ios::in);
employees.txt 是文本输入文件，所以用 ios::in。

fstream out("d:\\employees.dat", ios::out | ios::binary);
employees.dat 是输出文件，并且后面使用 write 按字节写结构体，所以要用 ios::out | ios::binary。

if (!in || !out)
判断两个文件是否成功打开。只要有一个失败，就输出错误并终止。

in.getline(buffer, 100);
in.getline(buffer, 100);
连续读取两行，通常是跳过文本文件开头的表头说明。

while (in >> emp.id >> emp.name >> emp.department >> emp.salary)
用文本格式读取一条员工记录。>> 会按空白分隔，所以 name 和 department 中不能含空格。

out.write((char*)&emp, sizeof(Employee));
把当前 Employee 对象按内存字节写入二进制文件。

out.write((char*)&defaultEmployee, sizeof(Employee));
循环结束后，再写入一个默认员工记录。后续读取二进制文件时可以把 id=0 或默认记录当作结束标志。

in.close();
out.close();
关闭输入和输出文件。
```

坑点：

```text
写二进制结构体要用 ios::binary，不要只写 ios::out。
write 的第一个参数必须是 char* 或 const char*，所以常见 (char*)&emp。
sizeof 后面要写结构体类型 Employee，或者写对象 emp；考试更常见 sizeof(Employee)。
getline(buffer, 100) 是读整行到 char 数组，不是 string 版本 getline(in, str)。
>> 读 char name[30] 时遇到空格停止，所以姓名如果有空格会被截断；基础考试通常默认没有空格。
defaultEmployee 是一个对象，写它要取地址：&defaultEmployee。
```

记忆：

```text
文本读字段用 >>，二进制存对象用 write。
写对象三件套：流.write((char*)&对象, sizeof(类型));
读对象三件套：流.read((char*)&对象, sizeof(类型));
```

### 27. 文件流成员函数总表

这一节专门补“考试突然问某个文件流函数是什么意思”的坑。以后看到文件操作题，先从这张表找函数归属。

| 函数/写法 | 作用 | 常考点 |
| --- | --- | --- |
| `open("文件名", 模式)` | 打开文件 | 可先定义流对象，再打开 |
| `close()` | 关闭文件 | 先写后读同一文件时尤其重要 |
| `is_open()` | 判断是否已经打开 | 常和 `if (!fin.is_open())` 搭配 |
| `operator!` / `if (!fin)` | 判断流是否失败 | 打开失败、读写失败都可能使流为假 |
| `good()` | 流状态完全正常 | 没有 eof/fail/bad |
| `eof()` | 是否到达文件尾 | 不推荐用 `while (!eof())` 控制读取 |
| `fail()` | 格式读取失败或操作失败 | 例如读 `int` 遇到非数字 |
| `bad()` | 严重 I/O 错误 | 比 `fail` 更严重 |
| `clear()` | 清除错误状态 | 清掉 fail/eof 后才能继续读写 |
| `getline(char*, n)` | 读一整行到字符数组 | 文件表头、姓名整行常考 |
| `getline(char*, n, delim)` | 读到指定分隔符 | `delim` 被取走但不存入数组 |
| `getline(stream, string)` | 读一整行到 `string` | 需要 `<string>` |
| `getline(stream, string, delim)` | 读到指定分隔符 | 非成员函数版本 |
| `width(n)` | 设置下一次输入/输出宽度 | `cin.width` 限制读入，`cout.width` 控制输出 |
| `ignore()` / `ignore(n, ch)` | 丢弃输入字符 | `>>` 后接 `getline` 常用 |
| `peek()` | 查看下一个字符但不取走 | 判断下一个字符 |
| `get(ch)` | 读一个字符，包括空格 | 和 `>> ch` 区分 |
| `get()` | 读一个字符并返回 | 返回值常用 `int` 接 |
| `get(char*, n)` | 读字符数组，遇换行停 | 换行通常留在流中 |
| `put(ch)` | 写一个字符 | 字符级输出 |
| `read((char*)&obj, size)` | 二进制读字节 | 第一个参数是 `char*` |
| `write((char*)&obj, size)` | 二进制写字节 | 结构体整块写常考 |
| `seekg(pos)` / `seekg(off, dir)` | 移动读指针 | g = get = 读 |
| `seekp(pos)` / `seekp(off, dir)` | 移动写指针 | p = put = 写 |
| `tellg()` | 返回读指针位置 | 求文件大小常见 |
| `tellp()` | 返回写指针位置 | 写入位置 |
| `flush()` | 刷新输出缓冲区 | 强制把缓冲内容写出去 |

#### 状态函数怎么理解

读文件最稳的循环是：

```cpp
int x;
while (fin >> x) {
    cout << x << endl;
}
```

不要优先写：

```cpp
while (!fin.eof()) {
    fin >> x;
    cout << x << endl;
}
```

原因是：`eof()` 通常要在一次读取失败之后才会变成真。先判断 `!eof()` 再读取，容易多处理一次旧数据。

如果读取失败后还想继续用这个流，常见步骤是：

```cpp
fin.clear();  // 清除错误状态
fin.ignore(); // 丢掉一个残留字符，具体题目可能要求 ignore(100, '\n')
```

#### `get` / `getline` / `>>` / `width` 区别

```cpp
char ch;
fin >> ch;     // 跳过空白，读一个非空白字符
fin.get(ch);   // 不跳过空白，空格和换行也能读到
```

```cpp
char buf[100];
fin.getline(buf, 100); // 读一行到字符数组
```

```cpp
string line;
getline(fin, line);    // 读一行到 string
```

```cpp
char s[10];
cin.width(5);
cin >> s; // 对 char 数组最多读 4 个普通字符，最后留给 '\0'
```

记忆：

```text
>> 按格式读，会跳空白。
get 按字符读，不放过空白。
getline 按整行读，读到换行停。
cin.width 限制下一次输入，cout.width 控制下一次输出。
```

#### `open` 和构造打开的关系

下面两种写法等价：

```cpp
ifstream fin("data.txt", ios::in);
```

```cpp
ifstream fin;
fin.open("data.txt", ios::in);
```

如果一个流已经打开了文件，通常不要直接再 `open()` 另一个文件，应先：

```cpp
fin.close();
fin.clear();
fin.open("other.txt", ios::in);
```

考试记忆：

```text
open 负责开，close 负责关；
is_open 看是否打开，!fin 看是否失败；
g 管读，p 管写；
二进制 read/write，文本 << >> / getline。
```

### 28. 文件关闭 `close`

```cpp
fin.close();
fout.close();
```

文件流对象析构时会自动关闭文件，但考试写程序题里建议手动写。

尤其是：

```text
先写文件，再读同一个文件
```

一定要先关闭写入流：

```cpp
ofstream fout("test.txt");
fout << "Data";
fout.close();

ifstream fin("test.txt");
```

### 29. 常见头文件总结

| 需求 | 头文件 |
| --- | --- |
| `cin`, `cout` | `<iostream>` |
| `ifstream`, `ofstream`, `fstream` | `<fstream>` |
| `istringstream`, `ostringstream`, `stringstream` | `<sstream>` |
| `setw`, `setfill`, `setprecision`, `setiosflags` | `<iomanip>` |
| `string` | `<string>` |

### 30. 常见选择题陷阱

| 陷阱 | 正误 | 解释 |
| --- | --- | --- |
| `setw` 持续生效 | 错 | `setw(n)` 只影响下一个输出项 |
| `setfill` 持续生效 | 对 | 后续再用宽度时仍按该字符填充 |
| `left/right` 持续生效 | 对 | 直到再次修改 |
| `fixed` 持续生效 | 对 | 后续浮点输出仍固定小数位 |
| `setprecision` 配合 `fixed` 和不配合含义一样 | 错 | 不配是有效数字，配了是小数位 |
| `ifstream` 用来写文件 | 错 | 基础语境下 `ifstream` 读文件 |
| `ofstream` 默认会清空文件 | 通常对 | 除非用 `ios::app` 等追加方式 |
| `>>` 读取字符串可以读整行 | 错 | 遇空白停止 |
| `getline` 和 `>>` 混用不用处理换行 | 错 | 常常要 `ignore()` |
| 二进制 `write` 第一个参数可以直接传 `double*` | 错 | 要转成 `char*` |
| `open()` 不需要指定读写方向 | 错 | `binary/ate` 只是附加模式，方向主要靠 `in/out` |
| `while (!fin.eof())` 是最佳读文件循环 | 错 | 容易多读一次，优先 `while (fin >> x)` |
| `get(ch)` 和 `>> ch` 完全一样 | 错 | `get` 不跳过空白，`>>` 会跳过空白 |

### 31. 图中题型秒杀

#### `istringstream`

```cpp
string Str1 = "This is a test";
string s1, s2, s3, s4;
istringstream input(Str1);
input >> s1 >> s2 >> s3 >> s4;
```

结果：

```text
s1 = "This"
s2 = "is"
s3 = "a"
s4 = "test"
```

如果问 `s1`，答案是 `This`。

#### `setfill('+') << setw(10) << setiosflags(ios::right) << "Data"`

`Data` 长度 4，宽度 10，右对齐，前面补 6 个 `+`：

```text
+++++Data
```

#### `setw(5)` 输出斐波那契

```cpp
cout << setw(5) << a0 << setw(5) << a1;
```

每个数字占 5 格，默认右对齐。如果数字是：

```text
0 1 1 2 3
```

视觉上是：

```text
    0    1    1    2    3
```

如果题目用 `-` 表示空格，就是：

```text
----0----1----1----2----3
```

### 32. 最后背诵版

```text
ifstream 读文件，ofstream 写文件，fstream 读写文件。
读用 ios::in，写用 ios::out，追加用 ios::app，二进制用 ios::binary。
打开文件先判断：if (!fin) 或 if (!fin.is_open())。
文本读写用 >> 和 <<，二进制读写用 read 和 write。
read/write 第一个参数要 char*，大小用 sizeof。
>> 自动跳过空白，读 string 遇空白停止。
getline 读整行，和 >> 混用要小心 ignore。
setw(n) 只管下一个输出项。
setfill、left/right、fixed、setprecision 会持续影响后续输出。
setprecision 单独用是有效数字，fixed + setprecision 是小数位。
dec/hex/oct 改整数进制，对后续整数持续生效。
seekg/tellg 管读指针，seekp/tellp 管写指针。
读文件循环优先写 while (fin >> x)，不要迷信 while (!fin.eof())。
```

再压成一句：

```text
读写分清 if/of/fstream，格式记住 setw 只一次；
fixed 配 precision 算小数，没 fixed 算有效数字；
文本用 << >>，二进制用 read/write；
g 是读指针，p 是写指针。
```

## C. 专题：类、对象、继承、派生与多态系统讲解

### 1. 总地图

类与对象这一章表面上知识点很多，其实可以压成一条主线：

```text
类是类型 -> 对象是实例 -> 成员有访问权限 -> 对象创建/销毁触发构造析构
继承产生“父子类” -> 基类指针/引用配合虚函数形成多态
```

考试最爱把这些点揉在一起考：

```text
构造/析构输出顺序
private/protected/public 访问是否合法
static/const/this 能不能用
值传参/引用传参是否拷贝
基类指针调用函数到底调用谁
派生类按值赋给基类是否切片
```

做题顺序建议固定下来：

```text
1. 先判断代码能不能编译。
2. 再看对象在哪里创建，构造函数怎么调用。
3. 再看传参方式：值、引用、指针。
4. 再看函数是否 virtual。
5. 最后按作用域结束顺序析构。
```

### 2. 类和对象的基本概念

类是自己定义的一种类型，对象是这种类型创建出来的变量。

```cpp
class Student {
private:
    int score;

public:
    void setScore(int s) {
        score = s;
    }

    int getScore() const {
        return score;
    }
};

int main() {
    Student stu;
    stu.setScore(90);
    return 0;
}
```

这里：

```text
Student 是类。
stu 是对象。
score 是数据成员。
setScore / getScore 是成员函数。
```

### 3. 访问权限：public / protected / private

访问权限决定“谁能直接碰这个成员”。

| 权限 | 类内 | 派生类内 | 类外 |
| --- | --- | --- | --- |
| `public` | 能访问 | 能访问 | 能访问 |
| `protected` | 能访问 | 能访问 | 不能访问 |
| `private` | 能访问 | 不能直接访问 | 不能访问 |

#### 典型题：判断哪些访问合法

```cpp
class Base {
public:
    int pub;

protected:
    int pro;

private:
    int pri;
};

class Derived : public Base {
public:
    void f() {
        pub = 1;  // 对
        pro = 2;  // 对

        // 错误示范：不能通过编译
        // pri = 3;
    }
};

int main() {
    Derived d;
    d.pub = 10;  // 对

    // 错误示范：不能通过编译
    // d.pro = 20;

    // 错误示范：不能通过编译
    // d.pri = 30;
}
```

答案：

```text
d.pub = 10 合法。
d.pro = 20 不合法。
d.pri = 30 不合法。
Derived 内部能访问 Base 的 public/protected，不能直接访问 Base 的 private。
```

陷阱：

```text
private 成员不是“不被继承”，而是“被继承了但派生类不能直接访问”。
```

### 4. `class` 和 `struct` 默认权限

```cpp
class A {
    int x;  // 默认 private
};

struct B {
    int x;  // 默认 public
};
```

继承时也有默认区别：

```cpp
class D1 : Base {};   // 默认 private 继承
struct D2 : Base {};  // 默认 public 继承
```

考试看到没写 `public` / `private` 的继承方式，要先看 `class` 还是 `struct`。

### 5. 构造函数

构造函数在对象创建时自动调用，用来初始化对象。

核心规则：

```text
构造函数名必须和类名相同。
构造函数没有返回类型，连 void 都不能写。
构造函数可以重载。
构造函数可以有默认参数，但不能造成二义性。
构造函数不能是 virtual。
构造函数不能是 const 成员函数。
构造函数可以是 private。
```

#### 典型题：判断写法是否合法

```cpp
class A {
public:
    A();          // 对
    A(int x);     // 对
    A(int x = 0); // 语法本身可以，但可能和 A() 造成二义性

    // 错误示范：不能通过编译
    void A();

    // 错误示范：不能通过编译
    virtual A();

    // 错误示范：不能通过编译
    A() const;
};
```

解析：

```text
void A() 错：构造函数没有返回类型。
virtual A() 错：构造函数不能是虚函数。
A() const 错：构造函数不能是 const 成员函数。
```

#### 默认构造函数陷阱

```cpp
class A {
public:
    A(int x) {}
};

int main() {
    // 错误示范：不能通过编译
    // A a;
}
```

你写了有参构造后，编译器不会再自动提供无参构造。

### 6. 析构函数

析构函数在对象生命周期结束时自动调用，用来释放资源。

核心规则：

```text
析构函数名是 ~类名。
析构函数没有返回类型。
析构函数没有参数。
析构函数不能重载。
析构函数可以是 virtual。
```

```cpp
class A {
public:
    ~A();       // 对

    // 错误示范：不能通过编译
    // ~A(int x);

    // 错误示范：不能通过编译
    // void ~A();
};
```

基类析构函数非常爱考：

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual ~Base() {
        cout << "~Base" << endl;
    }
};

class Derived : public Base {
public:
    ~Derived() {
        cout << "~Derived" << endl;
    }
};

int main() {
    Base* p = new Derived;
    delete p;
    return 0;
}
```

输出：

```text
~Derived
~Base
```

记忆：

```text
父指针删子对象，父析构要 virtual。
```

### 7. 拷贝构造和赋值

用已有对象创建新对象，调用拷贝构造；已有对象之间再赋值，调用赋值运算符。

```cpp
#include <iostream>
using namespace std;

class Box {
    int value;

public:
    Box(int v = 0) : value(v) {
        cout << "构造" << value << endl;
    }

    Box(const Box& other) : value(other.value) {
        cout << "拷贝构造" << value << endl;
    }

    Box& operator=(const Box& other) {
        cout << "赋值" << other.value << endl;
        value = other.value;
        return *this;
    }

    ~Box() {
        cout << "析构" << value << endl;
    }
};

int main() {
    Box a(10);
    Box b = a;
    Box c;
    c = a;
    return 0;
}
```

输出：

```text
构造10
拷贝构造10
构造0
赋值10
析构10
析构10
析构10
```

逐行解析：

```text
Box a(10)：普通构造。
Box b = a：用 a 初始化新对象 b，是拷贝构造。
Box c：默认构造。
c = a：c 已经存在，是赋值。
析构顺序和构造顺序相反：c、b、a。
```

陷阱：

```text
A b = a; 是拷贝构造，不是赋值。
b = a; 是赋值，因为 b 已经存在。
拷贝构造推荐写 A(const A& other)。
```

#### 补充：`<cstring>` 和 `char*` 深拷贝题

很多“补全 String 类”的题，表面考构造、拷贝、赋值、析构，实际一半在考 C 风格字符串。只要类里出现：

```cpp
char* pString;
int size;
```

就要立刻想到：

```text
strlen 算长度
new char[len + 1] 给 '\0' 留位置
strcpy 复制内容
delete[] 释放数组
```

C 风格字符串不是 `string` 对象，而是“字符序列 + 结尾的 `'\0'`”。

```cpp
char s1[] = "Hello";
const char* s2 = "World";
```

`"Hello"` 在内存里实际是：

```text
'H' 'e' 'l' 'l' 'o' '\0'
```

所以字符个数是 5，但存储空间至少要 6。

常用函数来自：

```cpp
#include <cstring>
```

| 函数 | 作用 | 考试坑点 |
| --- | --- | --- |
| `strlen(s)` | 求字符串长度 | 不包括结尾 `'\0'` |
| `strcpy(dest, src)` | 把 `src` 复制到 `dest` | `dest` 空间必须足够 |
| `strcmp(a, b)` | 比较字符串内容 | 相等返回 0 |
| `strcat(a, b)` | 把 `b` 拼接到 `a` 后面 | `a` 剩余空间必须足够 |

##### 构造函数固定写法

```cpp
Strings::Strings(const char* pN) {
    size = strlen(pN);
    pString = new char[size + 1];
    strcpy(pString, pN);
}
```

解析：

```text
strlen(pN) 不算 '\0'。
new char[size + 1] 是给 '\0' 多留一个位置。
strcpy 会把普通字符和结尾 '\0' 一起复制过去。
```

不能只写：

```cpp
pString = pN; // 错误思路：这只是拷贝地址，不是拷贝内容
```

这样会让 `pString` 指向别人的内存，后面 `delete[] pString` 很危险。

##### 拷贝构造固定写法

```cpp
Strings::Strings(const Strings& s) {
    size = s.size;
    pString = new char[size + 1];
    strcpy(pString, s.pString);
}
```

不能写：

```cpp
pString = s.pString; // 错误思路：浅拷贝
```

否则两个对象指向同一块字符数组，析构时会重复释放。

##### 赋值运算符固定写法

更规范的版本：

```cpp
Strings& Strings::operator=(const Strings& s) {
    if (this != &s) {
        delete[] pString;
        size = s.size;
        pString = new char[size + 1];
        strcpy(pString, s.pString);
    }

    return *this;
}
```

如果题目声明写成值传参：

```cpp
Strings& operator=(Strings);
```

就要按题目签名写：

```cpp
Strings& Strings::operator=(Strings s) {
    delete[] pString;
    size = s.size;
    pString = new char[size + 1];
    strcpy(pString, s.pString);
    return *this;
}
```

注意：值传参会先调用拷贝构造，生成形参副本。所以输出题里看到：

```cpp
Obj3 = Obj2 = Obj1;
```

要先按右结合理解：

```cpp
Obj3 = (Obj2 = Obj1);
```

并且每次调用 `operator=(Strings s)` 都会因为值传参而多一次拷贝构造。

##### 析构函数固定写法

```cpp
Strings::~Strings() {
    delete[] pString;
}
```

因为前面申请的是：

```cpp
new char[size + 1]
```

所以释放必须用：

```cpp
delete[] pString;
```

记忆：

```text
new 对 delete，new[] 对 delete[]。
```

##### 比较字符串内容不能用 `==`

```cpp
char a[] = "abc";
char b[] = "abc";

// 错误思路：比较地址，不是比较内容
// if (a == b)

if (strcmp(a, b) == 0) {
    cout << "same" << endl;
}
```

`strcmp` 结果：

```text
等于 0：两个字符串内容相等。
小于 0：前者字典序更小。
大于 0：前者字典序更大。
```

##### 一句话总背

```text
C 字符串靠 '\0' 结束；
strlen 不算 '\0'；
new char[strlen(s)+1] 给 '\0' 留位置；
strcpy 复制内容和 '\0'；
char* 成员必须深拷贝；
new[] 必须 delete[]；
比较内容用 strcmp，不用 ==。
```

### 8. 初始化列表

初始化列表在构造函数体执行前执行。

必须使用初始化列表的情况：

```text
const 成员
引用成员
没有默认构造函数的成员对象
调用基类有参构造函数
```

最阴的点：成员初始化顺序看声明顺序，不看初始化列表顺序。

```cpp
#include <iostream>
using namespace std;

class Demo {
    int x;
    int y;

public:
    Demo(int n) : y(n), x(y + 1) {
        cout << "x=" << x << ", y=" << y << endl;
    }
};

int main() {
    Demo d(5);
    return 0;
}
```

答案：

```text
x 的值不可靠，不能按 x=6, y=5 理解。
```

解析：

```text
声明顺序是 int x; int y;
所以先初始化 x，再初始化 y。
x(y + 1) 执行时，y 还没有被初始化。
```

记忆：

```text
初始化看声明，不看列表。
```

### 9. `this` 指针

普通成员函数里隐藏着一个 `this` 指针，指向当前调用该函数的对象。

```cpp
class Box {
    int length;

public:
    void setLength(int length) {
        this->length = length;
    }
};
```

`this->length` 是成员变量，右边的 `length` 是形参。

`this` 常见用途：

```text
区分同名成员和形参。
返回 *this 实现链式调用。
判断自赋值：if (this != &other)。
```

链式调用：

```cpp
class Counter {
    int value;

public:
    Counter& add(int n) {
        value += n;
        return *this;
    }
};
```

注意：

```text
static 成员函数没有 this。
this 本身不能改指向。
```

### 10. `const` 成员函数

`const` 成员函数承诺不修改普通数据成员。

```cpp
class A {
    int x;

public:
    int getX() const {
        return x;
    }

    void setX(int v) {
        x = v;
    }
};
```

`const` 对象只能调用 `const` 成员函数：

```cpp
const A a;
a.getX(); // 对

// 错误示范：不能通过编译
// a.setX(3);
```

特殊情况：

```text
mutable 成员可以在 const 成员函数中修改。
static 成员不属于某个对象，也可以在 const 成员函数中修改。
```

### 11. `static` 成员

`static` 成员属于类，不属于某个对象。

```cpp
#include <iostream>
using namespace std;

class Student {
    int score;
    static int count;

public:
    Student(int s) : score(s) {
        count++;
    }

    static void showCount() {
        cout << count << endl;

        // 错误示范：不能通过编译
        // cout << score << endl;
    }
};

int Student::count = 0;
```

核心规则：

```text
static 数据成员通常要类外定义。
static 成员函数没有 this。
static 成员函数不能直接访问普通成员。
static 成员函数不能是 const。
static 成员函数不能是 virtual。
```

#### 典型题：static 成员与 private 继承混合输出

题目：写出下面程序的运行结果，并判断哪些访问是合法的。

```cpp
#include <iostream>
using namespace std;

class Counter {
public:
    static void Increment() {
        count += 5;
    }

    static int count;

    void display() {
        cout << "Current count=" << count << endl;
    }
};

int Counter::count = 2;

class Derived : private Counter {
public:
    void update() {
        count = 20;
        Increment();
    }
};

int main() {
    Counter counter;
    Derived derived;

    counter.Increment();
    counter.display();

    derived.update();

    cout << "Current count=" << Counter::count << endl;
    cout << "Current count=" << counter.count << endl;

    return 0;
}
```

答案：

```text
Current count=7
Current count=25
Current count=25
```

逐行解析：

```text
int Counter::count = 2;
静态数据成员 count 属于 Counter 类，全体 Counter 对象以及派生类对象共享这一份。

Counter counter;
Derived derived;
这里只创建对象，不会改变 count，count 仍然是 2。

counter.Increment();
Increment 是 static 成员函数，虽然推荐写 Counter::Increment()，但用对象 counter.Increment() 调用也是合法的。
count += 5，所以 count 从 2 变成 7。

counter.display();
display 输出当前共享的静态成员 count，所以输出 Current count=7。

derived.update();
Derived 是 private 继承 Counter。基类的 public 成员到了 Derived 中对外变成 private，但在 Derived 的成员函数 update 内部可以访问。
count = 20; 把共享的 Counter::count 改成 20。
Increment(); 再加 5，所以共享的 count 变成 25。

cout << Counter::count;
count 在 Counter 中是 public static，因此可以通过类名访问，输出 25。

cout << counter.count;
static 成员也允许通过对象访问，虽然更推荐 Counter::count，输出仍然是同一份 count，也就是 25。
```

坑点：

```text
static 数据成员不是每个对象一份，而是整个类共享一份。
static 成员函数可以用 类名::函数名 调用，也可以用对象调用；考试通常都算合法。
private 继承不会复制一份新的 static 成员，只是改变继承成员对外的访问权限。
Derived 内部可以访问从 Counter 继承来的 count 和 Increment()。
类外不能写 derived.Increment() 或 derived.display()，因为 private 继承后这些成员在 Derived 对外是 private。
Counter::count 和 counter.count 访问的是同一份静态成员。
```

记忆：

```text
static 全类一份，不随对象分身。
private 继承改权限，不改成员归属。
```

### 12. 友元

友元可以访问类的私有成员，但友元不是成员函数，没有 `this`。

```cpp
#include <iostream>
using namespace std;

class Account {
    int balance;

public:
    Account(int b) : balance(b) {}

    friend void show(const Account& a);
};

void show(const Account& a) {
    cout << a.balance << endl;
}
```

陷阱：

```text
友元函数不是成员函数。
友元没有 this。
友元关系不传递。
友元关系不继承。
friend 写在 public/private 区都可以。
```

### 13. 值传参、引用传参、指针传参

```cpp
void f(A x);        // 值传参，拷贝一份
void g(A& x);       // 引用传参，不拷贝，可能修改实参
void h(const A& x); // const 引用，不拷贝，不修改实参
void p(A* x);       // 指针传参，不拷贝对象本身
```

考试输出题里，值传参最容易触发拷贝构造。

```cpp
void fun(Box x) {
    // x 是实参的副本
}
```

记忆：

```text
值传参拷一份，引用指针不拷贝。
const 引用常用于只读大对象。
```

### 14. 继承方式：public / protected / private

继承方式决定“基类 public/protected 成员到派生类中变成什么权限”。

| 继承方式 | 基类 public 到派生类 | 基类 protected 到派生类 | 基类 private |
| --- | --- | --- | --- |
| `public` | public | protected | 不可直接访问 |
| `protected` | protected | protected | 不可直接访问 |
| `private` | private | private | 不可直接访问 |

```cpp
class Base {
public:
    int pub;
protected:
    int pro;
private:
    int pri;
};

class D : private Base {
public:
    void f() {
        pub = 1; // 对，在 D 内部可访问，但变成 D 的 private
        pro = 2; // 对

        // 错误示范：不能通过编译
        // pri = 3;
    }
};
```

记忆：

```text
public 继承保持身份。
protected/private 继承会降级。
基类 private 成员被继承，但派生类不能直接访问。
```

### 15. 派生类构造析构顺序

构造：

```text
先基类 -> 再成员对象 -> 最后派生类构造函数体
```

析构：

```text
先派生类析构函数体 -> 再成员对象 -> 最后基类
```

典型题：

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    Base() { cout << "Base构造" << endl; }
    ~Base() { cout << "Base析构" << endl; }
};

class Member {
public:
    Member() { cout << "Member构造" << endl; }
    ~Member() { cout << "Member析构" << endl; }
};

class Derived : public Base {
    Member m;

public:
    Derived() { cout << "Derived构造" << endl; }
    ~Derived() { cout << "Derived析构" << endl; }
};

int main() {
    Derived d;
    return 0;
}
```

输出：

```text
Base构造
Member构造
Derived构造
Derived析构
Member析构
Base析构
```

多继承补充：

```text
多个基类的构造顺序看继承列表顺序，不看初始化列表顺序。
虚继承中，虚基类最先构造。
```

### 16. 多态三条件

运行时多态必须同时满足：

```text
1. 有继承关系。
2. 基类函数是 virtual。
3. 通过基类指针或引用调用。
```

典型题：

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual void show() {
        cout << "Base show" << endl;
    }

    void print() {
        cout << "Base print" << endl;
    }
};

class Derived : public Base {
public:
    void show() {
        cout << "Derived show" << endl;
    }

    void print() {
        cout << "Derived print" << endl;
    }
};

int main() {
    Derived d;
    Base* p = &d;

    p->show();
    p->print();

    return 0;
}
```

输出：

```text
Derived show
Base print
```

解析：

```text
show 是虚函数，通过 Base* 调用，看实际对象，输出 Derived show。
print 不是虚函数，通过 Base* 调用，看指针静态类型，输出 Base print。
```

### 17. 构造函数不能虚，析构函数可以虚

```cpp
class A {
public:
    // 错误示范：不能通过编译
    // virtual A();

    virtual ~A() {}
};
```

原因：

```text
构造时对象还没完整形成，不能靠虚函数机制构造。
析构常需要 virtual，尤其通过基类指针 delete 派生类对象时。
```

### 18. 构造/析构函数中调用虚函数

构造和析构期间调用虚函数，不会表现成完整派生类的多态效果。

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    Base() {
        show();
    }

    virtual void show() {
        cout << "Base" << endl;
    }
};

class Derived : public Base {
public:
    void show() {
        cout << "Derived" << endl;
    }
};

int main() {
    Derived d;
    return 0;
}
```

常按基础规则理解为输出：

```text
Base
```

因为构造 `Base` 部分时，`Derived` 部分还没构造完成。

记忆：

```text
构析中虚函数不虚。
```

### 19. 虚函数默认参数

虚函数函数体动态绑定，默认参数静态绑定。

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual void f(int x = 1) {
        cout << "Base " << x << endl;
    }
};

class Derived : public Base {
public:
    void f(int x = 2) override {
        cout << "Derived " << x << endl;
    }
};

int main() {
    Derived d;
    Base* p = &d;
    p->f();
    return 0;
}
```

输出：

```text
Derived 1
```

解析：

```text
函数体看实际对象：Derived。
默认参数看指针类型：Base*，所以默认值用 1。
```

### 20. 纯虚函数与抽象类

纯虚函数写法：

```cpp
virtual void f() = 0;
```

含有纯虚函数的类是抽象类，不能创建对象，但可以定义指针和引用。

```cpp
class Shape {
public:
    virtual void draw() = 0;
};

class Circle : public Shape {
public:
    void draw() override {}
};

int main() {
    // 错误示范：不能通过编译
    // Shape s;

    Circle c;
    Shape* p = &c; // 对
}
```

陷阱：

```text
抽象类不能实例化对象，但可以定义指针/引用。
纯虚函数也可以有函数体。
派生类没有实现全部纯虚函数，仍然是抽象类。
```

#### 典型题：抽象类引用形参触发多态

题目：写出下面程序的运行结果。

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    Base(int i) {
        value = i;
    }

    virtual void Print() = 0;

protected:
    int value;
};

class UpperCase : public Base {
public:
    UpperCase(int i) : Base(i) {}

    void Print() {
        cout << "Upper Case: " << (char)(value + 'A') << endl;
    }
};

class LowerCase : public Base {
public:
    LowerCase(int i) : Base(i) {}

    void Print() {
        cout << "Lower Case: " << (char)(value + 'a') << endl;
    }
};

class NumberCase : public Base {
public:
    NumberCase(int i) : Base(i) {}

    void Print() {
        cout << "Number Case: " << value << endl;
    }
};

void display(Base& b) {
    b.Print();
}

int main() {
    UpperCase u1(5);
    display(u1);

    LowerCase u2(5);
    display(u2);

    NumberCase u3(5);
    display(u3);

    return 0;
}
```

答案：

```text
Upper Case: F
Lower Case: f
Number Case: 5
```

逐行解析：

```text
Base 中有 virtual void Print() = 0，所以 Base 是抽象类，不能写 Base b(5)。

UpperCase u1(5);
先调用 Base(5)，把 value 设为 5，再构造 UpperCase 部分。

display(u1);
形参是 Base&，引用绑定到 UpperCase 对象，不发生切片。Print 是虚函数，所以动态绑定到 UpperCase::Print()。
value + 'A' 等于 5 + 'A'，也就是字母 F，所以输出 Upper Case: F。

LowerCase u2(5);
同理，Base(5) 把 value 设为 5。

display(u2);
Base& 绑定 LowerCase 对象，动态绑定到 LowerCase::Print()。
value + 'a' 等于 5 + 'a'，也就是字母 f，所以输出 Lower Case: f。

NumberCase u3(5);
同理，Base(5) 把 value 设为 5。

display(u3);
Base& 绑定 NumberCase 对象，动态绑定到 NumberCase::Print()，直接输出数字 5。
```

坑点：

```text
Base 是抽象类，不能创建 Base 对象，但可以写 Base&、Base*。
display(Base& b) 是引用传参，不会切片；如果写成 display(Base b)，不仅会切片，而且 Base 是抽象类，形参本身就非法。
Print 是纯虚函数，但派生类实现后，派生类对象可以正常创建。
'A' + 5 是字符运算，结果对应 F；'a' + 5 对应 f。
```

记忆：

```text
抽象类不能造对象，指针引用能上场。
纯虚函数派生补，基类引用调各方。
```

### 21. 重载、隐藏、覆盖

这三个词必须分清：

| 名称 | 条件 | 典型特点 |
| --- | --- | --- |
| 重载 overload | 同一作用域，函数名相同，参数不同 | 返回值不同不算重载 |
| 覆盖 override | 派生类重写基类虚函数，签名匹配 | 多态靠它 |
| 隐藏 hide | 派生类出现同名函数，隐藏基类同名函数 | 参数不同也会隐藏 |

```cpp
class Base {
public:
    virtual void f(int) {}
    void g() {}
};

class Derived : public Base {
public:
    void f(int) override {} // 覆盖
    void g(int) {}          // 隐藏 Base::g()
};
```

陷阱：

```text
返回值不同不能构成重载。
const 不一致可能导致没有真正覆盖。
参数不同通常是隐藏，不是覆盖。
override 可以帮你抓错签名。
```

### 22. 对象切片

派生类对象按值赋给基类对象，会丢掉派生类特有部分，叫对象切片。

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual void show() {
        cout << "Base" << endl;
    }
};

class Derived : public Base {
public:
    void show() override {
        cout << "Derived" << endl;
    }
};

void test(Base b) {
    b.show();
}

int main() {
    Derived d;

    Base b = d;
    b.show();

    test(d);

    Base& r = d;
    r.show();

    return 0;
}
```

输出：

```text
Base
Base
Derived
```

解析：

```text
Base b = d：切片，b 是真正的 Base 对象。
test(d)：按值传 Base 参数，切片。
Base& r = d：引用不切片，虚函数表现为 Derived。
```

记忆：

```text
多态对象别按值传，按值传就会切片。
```

#### 典型题：对象切片、引用、指针混合判断输出

题目：写出下面程序的运行结果。

```cpp
#include <iostream>
using namespace std;

class Shape {
public:
    Shape(int width = 0, int height = 0)
        : width(width), height(height) {}

    virtual void display() const {
        cout << "Shape: " << width << "x" << height << endl;
    }

protected:
    int width, height;
};

class Rectangle : public Shape {
public:
    Rectangle(int width = 0, int height = 0, int depth = 0)
        : Shape(width, height), depth(depth) {}

    void display() const override {
        cout << "Rectangle: " << width << "x" << height
             << "x" << depth << endl;
    }

private:
    int depth;
};

int main() {
    Rectangle rect(5, 10, 15);

    Shape s1 = rect;
    s1.display();

    Shape& s2 = rect;
    s2.display();

    Rectangle* r1 = &rect;
    r1->display();

    Shape* s3 = &rect;
    s3->display();

    return 0;
}
```

答案：

```text
Shape: 5x10
Rectangle: 5x10x15
Rectangle: 5x10x15
Rectangle: 5x10x15
```

逐行解析：

```text
Rectangle rect(5, 10, 15);
先构造一个真正的 Rectangle 对象，基类 Shape 部分保存 width=5, height=10，派生类部分保存 depth=15。

Shape s1 = rect;
用派生类对象初始化基类对象，发生对象切片。s1 是一个独立的 Shape 对象，只有 width 和 height，没有 depth。

s1.display();
s1 本身就是 Shape 对象，即使 display 是 virtual，也只能调用 Shape::display()。

Shape& s2 = rect;
s2 是基类引用，绑定到原来的 Rectangle 对象，没有切片。

s2.display();
通过基类引用调用虚函数，发生动态绑定，调用 Rectangle::display()。

Rectangle* r1 = &rect;
r1 是派生类指针，直接指向 Rectangle 对象。

r1->display();
指针静态类型和实际对象类型都是 Rectangle，调用 Rectangle::display()。

Shape* s3 = &rect;
s3 是基类指针，指向 Rectangle 对象，没有切片。

s3->display();
通过基类指针调用虚函数，发生动态绑定，调用 Rectangle::display()。
```

坑点：

```text
Shape s1 = rect;  看见“基类对象 = 派生类对象”，立刻想到对象切片。
Shape& s2 = rect; 看见“基类引用绑定派生类对象”，不切片，可以多态。
Shape* s3 = &rect; 看见“基类指针指向派生类对象”，不切片，可以多态。
virtual 只决定“通过基类指针/引用调用时能不能动态绑定”，不能阻止对象切片。
如果基类 display 没有 virtual，那么 s2.display() 和 s3->display() 都会调用 Shape::display()。
```

记忆：

```text
对象按值会切片，引用指针保真身。
虚函数看指针引用，切成基类就没派生。
```

### 23. 类与多态陷阱表

| 说法 | 对错 | 记忆 |
| --- | --- | --- |
| 构造函数可以有返回值 | 错 | 连 `void` 都不能写 |
| 构造函数可以重载 | 对 | 参数不同即可 |
| 构造函数可以是虚函数 | 错 | 构造不虚 |
| 析构函数可以是虚函数 | 对 | 析构可虚 |
| 析构函数可以重载 | 错 | 无参数 |
| `static` 成员函数有 `this` | 错 | static 无 this |
| `const` 对象能调用非 `const` 函数 | 错 | 只能调 const 成员函数 |
| private 成员不被继承 | 错 | 被继承但不能直接访问 |
| 基类指针指向派生类一定多态 | 错 | 还要 virtual |
| 抽象类不能定义指针 | 错 | 能定义指针/引用 |
| 派生类同名函数一定覆盖基类函数 | 错 | 可能隐藏 |
| 派生类对象赋给基类对象会切片 | 对 | 派生部分丢失 |

### 24. 最后背诵版

```text
类是类型，对象是实例。
class 默认 private，struct 默认 public。
构造同名无返回，析构名前加 ~。
构造可重载不可虚，析构无参可为虚。
拷贝构造是“用旧对象造新对象”，赋值是“已有对象再赋值”。
初始化顺序看声明顺序，不看初始化列表顺序。
this 指当前对象，static 无 this。
const 对象只调 const 函数，const 函数不改普通成员。
友元不是成员，无 this；友元不传递不继承。
继承中 private 被继承但不能直接访问。
构造顺序：基类 -> 成员 -> 派生类函数体。
析构顺序：派生类函数体 -> 成员 -> 基类。
多态三条件：继承、virtual、基类指针/引用。
构造不虚，析构可虚；父指针删子对象，父析构要 virtual。
同名不一定覆盖，参数不同多半隐藏。
多态对象别按值传，按值传就会切片。
```

## D. 专题：模板系统讲解

### 1. 总地图

模板是 C++ 的“泛型工具”。普通函数和普通类只能处理固定类型，模板可以让一份代码适配多种类型。

```text
函数模板：生成函数的模具。
类模板：生成类的模具。
模板实例化：编译器根据具体类型生成真正的函数或类。
```

例子：

```cpp
template <typename T>
T maxValue(T a, T b) {
    return a > b ? a : b;
}
```

这不是一个普通函数，而是函数模板。调用：

```cpp
maxValue(3, 5);       // 生成 int 版本
maxValue(3.1, 2.4);   // 生成 double 版本
```

### 2. 函数模板

基本格式：

```cpp
template <typename T>
返回类型 函数名(参数列表) {
    函数体
}
```

典型例子：

```cpp
#include <iostream>
using namespace std;

template <typename T>
T add(T a, T b) {
    return a + b;
}

int main() {
    cout << add(1, 2) << endl;
    cout << add(1.5, 2.5) << endl;
    return 0;
}
```

输出：

```text
3
4
```

解析：

```text
add(1, 2)：T 推导为 int。
add(1.5, 2.5)：T 推导为 double。
```

### 3. 函数模板实参推导

编译器会根据实参类型推导模板参数。

```cpp
template <typename T>
T maxValue(T a, T b) {
    return a > b ? a : b;
}

maxValue(10, 20);     // T = int
maxValue(1.2, 3.4);   // T = double
```

但下面可能出问题：

```cpp
// 错误示范：可能不能通过编译
// maxValue(10, 3.5);
```

因为一个参数像 `int`，另一个像 `double`，编译器不知道 `T` 到底该推导成谁。

可以显式指定：

```cpp
maxValue<double>(10, 3.5);
```

这样 `10` 会转换成 `double`。

### 4. 多个模板参数

```cpp
template <typename T1, typename T2>
void printPair(T1 a, T2 b) {
    cout << a << " " << b << endl;
}

printPair(1, 3.14); // T1 = int, T2 = double
```

多个类型不一样时，用多个模板参数。

### 5. `typename` 和 `class`

在模板参数列表里，下面两种写法基础语境下等价：

```cpp
template <typename T>
T f(T x) {
    return x;
}

template <class T>
T g(T x) {
    return x;
}
```

考试记忆：

```text
template <typename T> 和 template <class T> 在类型模板参数里基本等价。
```

### 6. 类模板

类模板是生成类的模具。

```cpp
template <typename T>
class Box {
private:
    T value;

public:
    Box(T v) : value(v) {}

    T get() const {
        return value;
    }
};
```

使用时必须指定模板实参：

```cpp
Box<int> a(10);
Box<double> b(3.14);
```

注意：

```cpp
// 错误示范：不能通过编译
// Box c(10);
```

基础考试里，类模板通常不能像函数模板那样省略模板参数。要写 `Box<int>`、`Box<double>`。

### 7. 类模板不是具体类型

```cpp
template <typename T>
class Container {
    // ...
};
```

这里的 `Container` 是模板名，不是具体类型。下面才是具体类型：

```cpp
Container<int>
Container<double>
Container<char>
```

记忆：

```text
Container 是模板，不是类型。
Container<int> 才是类型。
```

### 8. 典型题：类模板使用错误的是哪一个

```cpp
template <typename T>
class Container {
    /* ... */
};

// A
Container c;

// B
Container<double> DoubleContainer;

// C
int func(const Container<int>);

// D
template <typename T>
T func(const Container<T>*);
```

答案：**A**

逐项解析：

```cpp
Container c; // 错误示范：不能通过编译
```

`Container` 是类模板名，创建对象时必须指定模板实参。

```cpp
Container<double> DoubleContainer;
```

正确，`Container<double>` 是具体类型。

```cpp
int func(const Container<int>);
```

正确，函数参数类型已经写成 `Container<int>`。更高效写法是：

```cpp
int func(const Container<int>&);
```

```cpp
template <typename T>
T func(const Container<T>*);
```

正确，`T` 已经由函数模板参数列表引入，所以 `Container<T>` 合法。

### 9. 类模板对象、指针、引用、形参都要带实参

```cpp
template <typename T>
class Box {};

Box<int> a;          // 对
Box<double>* p;      // 对
Box<char>& r = obj;  // 对，前提是 obj 是 Box<char>
void f(Box<int> b);  // 对

Box b;               // 错误示范：不能通过编译
Box* p2;             // 错误示范：不能通过编译
void g(Box x);       // 错误示范：不能通过编译
```

原因：

```text
Box 只是模板名。
Box<int> 才是具体类型。
```

### 10. 类模板成员函数在类外定义

如果成员函数写在类外，每个成员函数定义前也要写模板声明。

```cpp
template <typename T>
class Box {
private:
    T value;

public:
    Box(T v);
    T get() const;
};

template <typename T>
Box<T>::Box(T v) : value(v) {}

template <typename T>
T Box<T>::get() const {
    return value;
}
```

陷阱：

```text
类外定义时，不是 Box::get，而是 Box<T>::get。
每个类外成员函数定义前都要写 template <typename T>。
```

### 11. 函数模板和类模板配合

如果函数只接受某一种具体容器：

```cpp
int sum(const Container<int>& c);
```

如果函数希望接受任意 `T` 的容器：

```cpp
template <typename T>
T sum(const Container<T>& c);
```

区别：

```text
Container<int>：固定 T 是 int。
Container<T>：T 是函数模板参数，调用时再决定。
```

### 12. 非类型模板参数

模板参数不一定是类型，也可以是整数常量等。

```cpp
template <typename T, int N>
class Array {
private:
    T data[N];

public:
    int size() const {
        return N;
    }
};

Array<int, 10> a;
Array<double, 5> b;
```

`N` 必须是编译期能确定的常量。

### 13. 模板实例化

模板本身只是模具，只有使用具体类型时，编译器才生成对应代码。

```cpp
template <typename T>
T square(T x) {
    return x * x;
}

int a = square(3);       // 实例化 int square(int)
double b = square(1.5);  // 实例化 double square(double)
```

记忆：

```text
模板不是直接运行的代码，实例化后才生成具体函数/类。
```

### 14. 模板代码为什么常写在头文件

模板需要在实例化时看到完整定义。只看到声明通常不够。

```cpp
template <typename T>
T add(T a, T b); // 只有声明
```

如果另一个文件调用：

```cpp
add(1, 2);
```

编译器需要看到 `add` 的函数体，才能生成 `int add(int, int)`。

考试记忆：

```text
模板定义通常放在头文件或同一文件中。
模板只放声明、定义藏在 cpp 里，容易链接失败。
```

### 15. 模板与 `static` 成员

类模板的静态成员是“每个实例化类型各有一份”。

```cpp
template <typename T>
class Counter {
public:
    static int count;
};

template <typename T>
int Counter<T>::count = 0;

int main() {
    Counter<int>::count = 1;
    Counter<double>::count = 2;
}
```

`Counter<int>::count` 和 `Counter<double>::count` 是两份不同的静态成员。

### 16. 模板与继承、多态

模板是编译期机制，多态通常是运行期机制。它们可以一起用，但不要混淆。

```cpp
template <typename T>
class Holder {
    T value;
};
```

`Holder<Base*>` 可以存基类指针，基类指针再指向派生类对象时，可以发生多态：

```cpp
class Base {
public:
    virtual void f() {}
};

class Derived : public Base {
public:
    void f() override {}
};

Holder<Base*> h;
```

考试基础层面记：

```text
模板解决“类型泛化”。
虚函数解决“运行时多态”。
模板不等于虚函数，多态不等于模板。
```

### 17. 模板与友元

基础题常见两种写法：

```cpp
template <typename T>
class Box {
    T value;

public:
    Box(T v) : value(v) {}

    friend void show(Box<T>& b) {
        cout << b.value << endl;
    }
};
```

这种友元函数对当前 `Box<T>` 直接有效。

更复杂的“友元函数模板”基础考试一般不深挖，只要记住：

```text
友元仍然不是成员函数。
模板友元也没有 this。
需要访问 private 时可用 friend。
```

### 18. 模板重载

函数模板可以和普通函数同时存在。

```cpp
#include <iostream>
using namespace std;

template <typename T>
void print(T x) {
    cout << "template" << endl;
}

void print(int x) {
    cout << "int" << endl;
}

int main() {
    print(1);
    print(1.5);
    return 0;
}
```

输出：

```text
int
template
```

解析：

```text
print(1)：普通函数 void print(int) 更匹配。
print(1.5)：用函数模板 T = double。
```

### 19. 模板陷阱表

| 说法 | 对错 | 记忆 |
| --- | --- | --- |
| 类模板本身就是具体类型 | 错 | `Container<int>` 才是类型 |
| 类模板对象可以不写模板实参 | 错 | 基础语境下必须写 |
| `template <typename T>` 和 `template <class T>` 完全不能替换 | 错 | 类型参数里基本等价 |
| 函数模板调用时常能自动推导 T | 对 | 由实参推导 |
| 函数模板所有混合类型调用都能自动推导 | 错 | `f(1, 2.5)` 可能推导冲突 |
| 类模板成员函数类外定义要写 `Box<T>::` | 对 | 不能只写 `Box::` |
| 模板定义通常放头文件/同一文件 | 对 | 实例化时要看到定义 |
| 类模板不同实参的静态成员共享一份 | 错 | 每个实例化类型各一份 |
| 模板就是运行时多态 | 错 | 模板多为编译期机制 |

### 20. 最后背诵版

```text
模板是模具，实例化后才生成具体代码。
函数模板能自动推导，类模板通常要显式写实参。
typename 和 class 在类型模板参数中基本等价。
Container 不是类型，Container<int> 才是类型。
对象、指针、引用、函数形参使用类模板时都要带实参。
函数模板里可以写 Container<T>，因为 T 已由 template <typename T> 引入。
类模板成员函数类外定义：template <typename T> 返回类型 类名<T>::函数名。
模板定义通常放头文件或同一文件中。
非类型模板参数必须是编译期常量。
类模板静态成员：不同 T 各有一份。
模板管类型泛化，虚函数管运行时多态。
```

## 0. 读程序输出题总套路

### 考法定位

读程序输出题通常不是考语法记忆，而是考你能不能按对象生命周期排队。先找对象在哪里创建，再看是普通构造、拷贝构造还是赋值，最后按作用域结束顺序倒着析构。

这类题最容易被函数传参、函数返回、临时对象、局部对象绕进去。做题时不要一眼猜输出，先在代码旁边标出每个对象的出生和死亡。

### 典型题：写出输出结果

```cpp
#include <iostream>
using namespace std;

class Trace {
    int id;

public:
    Trace(int n) : id(n) {
        cout << "构造" << id << endl;
    }

    Trace(const Trace& other) : id(other.id) {
        cout << "拷贝" << id << endl;
    }

    ~Trace() {
        cout << "析构" << id << endl;
    }
};

void test(Trace x) {
    Trace y(2);
    cout << "函数体" << endl;
}

int main() {
    Trace a(1);
    test(a);
    cout << "main结束前" << endl;
    return 0;
}
```

### 答案

```text
构造1
拷贝1
构造2
函数体
析构2
析构1
main结束前
析构1
```

### 解析

`Trace a(1);` 创建对象 `a`，调用普通构造函数，输出 `构造1`。

`test(a);` 的形参是 `Trace x`，属于按值传参，所以要用 `a` 拷贝出形参对象 `x`，输出 `拷贝1`。

进入 `test` 后，`Trace y(2);` 创建局部对象 `y`，输出 `构造2`，然后执行函数体输出 `函数体`。

函数结束时，局部对象按后构造先析构的顺序销毁，先析构 `y`，再析构形参 `x`，所以输出 `析构2`、`析构1`。

回到 `main` 后输出 `main结束前`。最后 `main` 结束，局部对象 `a` 析构，输出最后一个 `析构1`。

### 坑点

- 按值传参会产生一个新对象。
- 引用传参不会产生新对象。
- 函数内局部对象离开函数立即析构。
- 同样输出 `析构1` 不代表是同一个对象，要看对象身份。
- 输出题先数对象，再排顺序。

### 本章速记

1. 先看对象创建语句。
2. 再看传参方式：值传参拷贝，引用/指针传参不拷贝对象本身。
3. 最后看作用域：谁先结束，谁先析构。

## 1. 构造函数阴招

### 考法定位

构造函数常考判断题和改错题。核心特征是：函数名与类名相同，没有返回类型，创建对象时自动调用，可以重载，可以带默认参数，但不能是虚函数，也不能写成 `const` 成员函数。

选择题里常把“没有返回值”和“返回值是 `void`”混在一起。注意：构造函数不是返回 `void`，而是根本不写返回类型。

### 典型题：判断下列写法是否合法

```cpp
class Student {
public:
    Student();                    // 合法：默认构造函数
    Student(int age);             // 合法：有参构造函数
    Student(int age, int id = 0); // 合法：构造函数可以有默认参数

    // 错误示范：不能通过编译
    void Student();

    // 错误示范：不能通过编译
    virtual Student();

    // 错误示范：不能通过编译
    Student() const;
};
```

### 答案

前三个声明合法，后三个声明非法。

### 解析

`Student();` 是无参构造函数。没有写返回类型，函数名和类名一致。

`Student(int age);` 和 `Student(int age, int id = 0);` 说明构造函数可以重载，也可以带默认参数。

`void Student();` 错在写了返回类型。只要写了 `void`，它就不是合法构造函数声明。

`virtual Student();` 错在构造函数不能是虚函数。对象还没构造完整，不能依赖多态机制。

`Student() const;` 错在构造函数不能是 `const` 成员函数。构造阶段本来就是初始化对象状态。

### 补充题：默认参数导致二义性

```cpp
class A {
public:
    A() {}
    A(int x = 0) {}
};

int main() {
    // 错误示范：不能通过编译
    A a;
    return 0;
}
```

### 答案

不能通过编译。

### 解析

`A a;` 既可以调用 `A()`，也可以调用 `A(int x = 0)`，编译器无法判断该选哪个，所以产生二义性。

### 坑点

- 构造函数没有返回类型，连 `void` 也不能写。
- 构造函数名必须与类名完全相同，大小写不同也不行。
- 构造函数可以重载。
- 构造函数可以有默认参数，但不能造成二义性。
- 写了有参构造后，编译器不一定再自动生成无参构造。
- 构造函数不能是 `virtual`。
- 构造函数不能写成 `const` 成员函数。
- 构造函数可以是 `private`，例如单例模式中常见。

## 2. 析构函数阴招

### 考法定位

析构函数常考三个点：名字前有 `~`，没有返回类型，没有参数，不能重载。它在对象生命周期结束时自动调用，析构顺序和构造顺序相反。

如果类要作为基类使用，并且可能通过基类指针删除派生类对象，基类析构函数应该写成虚析构函数。

### 典型题：写出输出结果

```cpp
#include <iostream>
using namespace std;

class Demo {
    int id;

public:
    Demo(int n) : id(n) {
        cout << "构造" << id << endl;
    }

    ~Demo() {
        cout << "析构" << id << endl;
    }
};

int main() {
    Demo a(1);
    Demo b(2);
    cout << "中间" << endl;
    return 0;
}
```

### 答案

```text
构造1
构造2
中间
析构2
析构1
```

### 解析

`a` 先构造，输出 `构造1`。`b` 后构造，输出 `构造2`。

程序执行到 `cout << "中间"`，输出 `中间`。

`main` 结束时，局部对象销毁。析构顺序和构造顺序相反，后构造的 `b` 先析构，再析构 `a`。

### 补充题：析构函数的非法写法

```cpp
class A {
public:
    ~A();       // 合法

    // 错误示范：不能通过编译
    int ~A();

    // 错误示范：不能通过编译
    ~A(int x);
};
```

### 答案

只有 `~A();` 合法。

### 解析

析构函数没有返回类型，不能写 `int`、`void` 等返回类型。析构函数也不能带参数，所以不能重载。

### 坑点

- 析构函数没有返回类型。
- 析构函数没有参数。
- 析构函数不能重载。
- 析构顺序通常是后构造的先析构。
- 构造函数不能是虚函数，析构函数可以是虚函数。
- 父类指针删除子类对象时，父类析构函数应写成 `virtual`。

## 3. 拷贝构造与赋值阴招

### 考法定位

这一章最容易把“初始化”和“赋值”混在一起。用已有对象创建新对象，调用拷贝构造；对象已经存在，再把另一个对象赋给它，调用赋值运算符。

考试经常用 `A b = a;` 和 `b = a;` 区分这两个概念。前者是初始化，后者是赋值。

### 典型题：写出输出结果

```cpp
#include <iostream>
using namespace std;

class Box {
    int value;

public:
    Box(int v = 0) : value(v) {
        cout << "构造" << value << endl;
    }

    Box(const Box& other) : value(other.value) {
        cout << "拷贝构造" << value << endl;
    }

    Box& operator=(const Box& other) {
        cout << "赋值" << other.value << endl;
        value = other.value;
        return *this;
    }

    ~Box() {
        cout << "析构" << value << endl;
    }
};

int main() {
    Box a(10);
    Box b = a;
    Box c;
    c = a;
    return 0;
}
```

### 答案

```text
构造10
拷贝构造10
构造0
赋值10
析构10
析构10
析构10
```

### 解析

`Box a(10);` 创建新对象 `a`，调用普通构造函数。

`Box b = a;` 虽然有等号，但这是用 `a` 初始化新对象 `b`，调用拷贝构造函数。

`Box c;` 创建新对象 `c`，调用默认构造函数，默认值为 `0`。

`c = a;` 此时 `c` 已经存在，所以不是拷贝构造，而是调用赋值运算符。

函数结束时，局部对象按后构造先析构的顺序销毁。构造顺序是 `a`、`b`、`c`，析构顺序是 `c`、`b`、`a`。由于 `c` 赋值后 `value` 变成 `10`，所以三个析构都输出 `析构10`。

### 补充题：按值传参触发拷贝构造

```cpp
#include <iostream>
using namespace std;

class A {
public:
    A() {
        cout << "构造" << endl;
    }

    A(const A&) {
        cout << "拷贝构造" << endl;
    }
};

void fun(A x) {
    cout << "fun" << endl;
}

int main() {
    A a;
    fun(a);
    return 0;
}
```

### 答案

```text
构造
拷贝构造
fun
```

### 解析

`A a;` 调用默认构造。`fun(a);` 的形参是 `A x`，按值传参会用实参 `a` 拷贝出形参 `x`，所以调用拷贝构造。

### 坑点

- `Box b = a;` 是拷贝构造，不是赋值。
- `b = a;` 是赋值，因为 `b` 已经存在。
- 拷贝构造的典型写法是 `Box(const Box& other)`。
- 拷贝构造如果写成 `Box(Box other)` 会导致为了传参又要拷贝，形成递归问题。
- 赋值运算符通常返回 `*this` 的引用，即 `Box&`。
- 类中有裸指针资源时，要特别小心默认拷贝和默认赋值造成浅拷贝。

## 4. 返回引用和生命周期阴招

### 考法定位

这一章主要考“对象还活不活着”。返回引用不会拷贝对象，但必须保证被引用的对象在函数返回后仍然存在。

最典型的陷阱是返回局部变量的引用。局部变量在函数结束时已经析构，再返回它的引用，就是悬空引用。

### 典型题：找出错误

```cpp
#include <iostream>
using namespace std;

class A {
    int value;

public:
    A(int v = 0) : value(v) {}

    int get() const {
        return value;
    }
};

A& makeA() {
    A temp(10);

    // 错误示范：不能通过编译或产生严重警告，运行行为不可靠
    return temp;
}

int main() {
    A& r = makeA();
    cout << r.get() << endl;
    return 0;
}
```

### 答案

错误在 `return temp;`。不能返回局部对象的引用。

### 解析

`temp` 是 `makeA` 函数内部的局部对象。函数执行结束时，`temp` 的生命周期结束，对象被销毁。

返回类型是 `A&`，表示返回对象引用。可是函数返回后，被引用的 `temp` 已经不存在了，`r` 就变成悬空引用。继续访问 `r.get()` 属于不可靠行为。

### 补充题：返回 `*this` 实现链式调用

```cpp
#include <iostream>
using namespace std;

class Counter {
    int value;

public:
    Counter(int v = 0) : value(v) {}

    Counter& add(int n) {
        value += n;
        return *this;
    }

    void print() const {
        cout << value << endl;
    }
};

int main() {
    Counter c;
    c.add(1).add(2).add(3);
    c.print();
    return 0;
}
```

### 答案

```text
6
```

### 解析

`add` 返回的是 `Counter&`，也就是当前对象本身的引用。`c.add(1)` 返回 `c`，于是可以继续 `.add(2)` 和 `.add(3)`。

这里返回 `*this` 是安全的，因为 `c` 是 `main` 中的局部对象，在整条链式调用期间仍然存在。

### 坑点

- 返回引用不产生拷贝，但引用对象必须还活着。
- 不能返回局部变量的引用。
- 不能返回局部变量的地址。
- 可以返回全局对象、静态对象、成员对象或 `*this` 的引用，但要确保生命周期足够长。
- `return *this;` 常用于链式调用，和 `return 局部变量引用;` 完全不同。

## 5. 初始化列表阴招

### 考法定位

初始化列表常考两个方向：一是哪些成员必须在初始化列表中初始化，二是成员初始化顺序到底看哪里。

记住一句话：初始化列表负责“初始化”，构造函数体里通常是“赋值”。`const` 成员、引用成员、没有默认构造函数的成员对象，必须用初始化列表。

### 典型题：判断程序输出

```cpp
#include <iostream>
using namespace std;

class Demo {
    int x;
    int y;

public:
    Demo(int n) : y(n), x(y + 1) {
        cout << "x=" << x << ", y=" << y << endl;
    }
};

int main() {
    Demo d(5);
    return 0;
}
```

### 答案

输出结果不可靠，`x` 的值不确定，不能按 `x=6, y=5` 理解。

### 解析

类中成员声明顺序是：

```cpp
int x;
int y;
```

所以实际初始化顺序是先初始化 `x`，再初始化 `y`。虽然初始化列表写的是 `y(n), x(y + 1)`，但这个书写顺序不决定初始化顺序。

初始化 `x(y + 1)` 时，`y` 还没有被初始化，所以 `x` 得到的是不确定值。之后才初始化 `y(n)`。

### 补充题：必须使用初始化列表

```cpp
class A {
    const int x;
    int& ref;

public:
    A(int n, int& r) : x(n), ref(r) {
    }
};
```

### 答案

这段写法正确。

### 解析

`x` 是 `const int`，必须在初始化列表中初始化，不能在构造函数体内赋值。

`ref` 是引用成员，也必须在初始化列表中绑定到某个对象，不能先声明后赋值。

### 错误示范

```cpp
class A {
    const int x;
    int& ref;

public:
    A(int n, int& r) {
        // 错误示范：不能通过编译
        x = n;

        // 错误示范：不能通过编译
        ref = r;
    }
};
```

### 坑点

- 成员初始化顺序看声明顺序，不看初始化列表顺序。
- 不要在初始化列表里用后声明的成员初始化先声明的成员。
- `const` 成员必须初始化，不能后赋值。
- 引用成员必须初始化，不能后绑定。
- 没有默认构造函数的成员对象必须在初始化列表中初始化。
- 调用基类有参构造也要写在初始化列表中。

## 6. 对象构造与析构顺序阴招

### 考法定位

构造析构顺序是读程序输出题高频考点。只要看到继承、成员对象、局部对象混在一起，就要按固定顺序分析。

构造顺序：先基类，再成员对象，最后执行本类构造函数体。析构顺序反过来：先执行本类析构函数体，再析构成员对象，最后析构基类。

### 典型题：写出输出结果

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    Base() {
        cout << "Base构造" << endl;
    }

    ~Base() {
        cout << "Base析构" << endl;
    }
};

class Member {
public:
    Member() {
        cout << "Member构造" << endl;
    }

    ~Member() {
        cout << "Member析构" << endl;
    }
};

class Derived : public Base {
    Member m;

public:
    Derived() {
        cout << "Derived构造" << endl;
    }

    ~Derived() {
        cout << "Derived析构" << endl;
    }
};

int main() {
    Derived d;
    return 0;
}
```

### 答案

```text
Base构造
Member构造
Derived构造
Derived析构
Member析构
Base析构
```

### 解析

创建 `Derived d;` 时，先构造基类部分 `Base`，输出 `Base构造`。

然后构造成员对象 `m`，输出 `Member构造`。

最后执行 `Derived` 构造函数体，输出 `Derived构造`。

程序结束时析构顺序相反。先执行 `Derived` 析构函数体，再析构成员对象 `m`，最后析构基类 `Base`。

### 补充题：多个成员对象的顺序

```cpp
#include <iostream>
using namespace std;

class A {
public:
    A(const char* name) {
        cout << name << "构造" << endl;
    }

    ~A() {
        cout << "A析构" << endl;
    }
};

class Test {
    A first;
    A second;

public:
    Test() : second("second"), first("first") {
        cout << "Test构造" << endl;
    }
};

int main() {
    Test t;
    return 0;
}
```

### 答案

```text
first构造
second构造
Test构造
A析构
A析构
```

### 解析

虽然初始化列表中写的是 `second("second"), first("first")`，但成员声明顺序是 `first` 在前，`second` 在后，所以先构造 `first`，再构造 `second`。

析构时顺序相反，先析构 `second`，再析构 `first`。由于析构函数里没有保存名字，只统一输出 `A析构`，所以只能看到两个相同的析构输出。

### 坑点

- 派生类构造函数体不是最先执行的。
- 成员对象在本类构造函数体之前构造。
- 析构顺序是完整反过来。
- 成员对象的析构发生在本类析构函数体之后。
- 多继承构造顺序看继承列表顺序，不看初始化列表顺序。
- 虚继承中虚基类最先构造。

## 7. 全局、静态、局部静态对象阴招

### 考法定位

这一章考生命周期。普通局部对象离开作用域就析构；全局对象和静态对象生命周期更长，通常到程序结束才析构。

局部静态对象最容易考：它不是进入 `main` 前构造，而是第一次执行到定义语句时构造，并且只构造一次。

### 典型题：写出输出结果

```cpp
#include <iostream>
using namespace std;

class A {
    const char* name;

public:
    A(const char* n) : name(n) {
        cout << name << "构造" << endl;
    }

    ~A() {
        cout << name << "析构" << endl;
    }
};

A globalObj("全局对象");

void fun() {
    static A staticObj("局部静态对象");
    A localObj("普通局部对象");
    cout << "fun函数体" << endl;
}

int main() {
    cout << "main开始" << endl;
    fun();
    cout << "第二次调用" << endl;
    fun();
    cout << "main结束前" << endl;
    return 0;
}
```

### 答案

```text
全局对象构造
main开始
局部静态对象构造
普通局部对象构造
fun函数体
普通局部对象析构
第二次调用
普通局部对象构造
fun函数体
普通局部对象析构
main结束前
局部静态对象析构
全局对象析构
```

### 解析

`globalObj` 是全局对象，在 `main` 执行前构造，所以第一行输出 `全局对象构造`。

第一次调用 `fun()` 时，程序第一次执行到 `static A staticObj("局部静态对象");`，所以构造局部静态对象。接着创建普通局部对象 `localObj`。

`fun` 结束时，普通局部对象 `localObj` 立即析构。但局部静态对象不会在函数结束时析构，它会活到程序结束。

第二次调用 `fun()` 时，`staticObj` 已经构造过，不会再次构造，只会重新创建普通局部对象 `localObj`。

`main` 结束后，静态生命周期对象析构。通常局部静态对象比全局对象后构造，所以先析构局部静态对象，再析构全局对象。

### 坑点

- 全局对象在 `main` 前构造，在 `main` 后析构。
- 普通局部对象每次进入作用域都会构造，离开作用域就析构。
- 局部静态对象第一次执行到定义处才构造。
- 局部静态对象只构造一次。
- 局部静态对象不是函数结束就析构，而是程序结束时析构。
- 不同源文件里的全局对象构造顺序不要轻易假定。

## 8. const 成员函数阴招

### 考法定位

`const` 成员函数常考两件事：第一，`const` 对象只能调用 `const` 成员函数；第二，`const` 成员函数内部不能修改普通成员变量。读题时重点看函数声明末尾有没有 `const`，它修饰的是隐藏的 `this` 指针。

### 典型题：判断下列调用是否合法

```cpp
#include <iostream>
using namespace std;

class Counter {
private:
    int value;
    mutable int visitTimes;
    static int totalVisits;

public:
    Counter(int v = 0) : value(v), visitTimes(0) {}

    void setValue(int v) {
        value = v;
    }

    int getValue() const {
        visitTimes++;
        totalVisits++;
        return value;
    }

    void wrongChange() const {
        // 错误示范：不能通过编译
        // value = 100;
    }
};

int Counter::totalVisits = 0;

int main() {
    Counter a(10);
    const Counter b(20);

    a.setValue(30);
    cout << a.getValue() << endl;

    cout << b.getValue() << endl;

    // 错误示范：不能通过编译
    // b.setValue(40);

    return 0;
}
```

### 答案

```text
30
20
```

`b.setValue(40)` 不合法，因为 `b` 是 `const` 对象，只能调用 `const` 成员函数。

### 解析

`getValue()` 后面有 `const`，所以它可以被普通对象和 `const` 对象调用。

`setValue()` 后面没有 `const`，所以它不能被 `const Counter b` 调用。

`visitTimes` 被声明为 `mutable`，即使在 `const` 成员函数中也可以修改。

`totalVisits` 是静态成员，属于类，不属于某个对象，因此也可以在 `const` 成员函数中修改。

### 坑点

- `void f() const` 的 `const` 写在函数参数列表后面。
- `const` 对象只能调用 `const` 成员函数。
- `const` 成员函数不能修改普通数据成员。
- `mutable` 成员可以在 `const` 成员函数中修改。
- 静态成员不属于具体对象，`const` 成员函数可以修改非 `const` 静态成员。
- `const` 可以参与成员函数重载：`void f();` 和 `void f() const;` 可以同时存在。

## 9. static 成员阴招

### 考法定位

`static` 成员的核心是“属于类，不属于对象”。静态数据成员全类共享一份；静态成员函数没有 `this` 指针，所以不能直接访问普通成员，也不能声明为 `const` 或 `virtual`。

### 典型题：写出程序输出，并判断错误语句

```cpp
#include <iostream>
using namespace std;

class Student {
private:
    int score;
    static int count;

public:
    Student(int s) : score(s) {
        count++;
    }

    void showScore() const {
        cout << "score=" << score << endl;
    }

    static void showCount() {
        cout << "count=" << count << endl;

        // 错误示范：不能通过编译
        // cout << score << endl;
    }

    // 错误示范：不能通过编译
    // static void wrong() const {}
};

int Student::count = 0;

int main() {
    Student s1(80);
    Student s2(90);

    s1.showScore();
    Student::showCount();

    return 0;
}
```

### 答案

```text
score=80
count=2
```

### 解析

创建 `s1` 时，构造函数执行一次，`count` 变为 `1`。

创建 `s2` 时，构造函数再次执行，`count` 变为 `2`。

`showScore()` 是普通成员函数，可以访问普通成员 `score`。

`showCount()` 是静态成员函数，只能直接访问静态成员 `count`。如果要访问普通成员，必须通过某个对象，例如 `obj.score`。

### 坑点

- 静态数据成员通常要在类外定义：`int Student::count = 0;`
- 静态成员函数没有 `this` 指针。
- 静态成员函数不能直接访问非静态成员。
- 静态成员函数不能写成 `const`。
- 静态成员函数不能是虚函数。
- 静态成员属于类，全体对象共享一份。

## 10. this 指针阴招

### 考法定位

`this` 指针表示“当前调用这个成员函数的对象”。考试常考成员名和形参名重名、返回 `*this` 实现链式调用、静态函数没有 `this`。

### 典型题：写出程序输出

```cpp
#include <iostream>
using namespace std;

class Box {
private:
    int length;
    int width;

public:
    Box(int length = 0, int width = 0) {
        this->length = length;
        this->width = width;
    }

    Box& setLength(int length) {
        this->length = length;
        return *this;
    }

    Box& setWidth(int width) {
        this->width = width;
        return *this;
    }

    void show() const {
        cout << length << " " << width << endl;
    }

    static void wrong() {
        // 错误示范：不能通过编译
        // this->length = 10;
    }
};

int main() {
    Box b(2, 3);
    b.show();

    b.setLength(8).setWidth(6);
    b.show();

    return 0;
}
```

### 答案

```text
2 3
8 6
```

### 解析

构造函数参数 `length` 和成员变量 `length` 同名，因此用 `this->length` 表示当前对象的成员。

`setLength()` 返回 `Box&`，并返回 `*this`，所以可以继续调用 `.setWidth(6)`。

`b.setLength(8).setWidth(6)` 是链式调用，本质是先修改 `b.length`，再继续修改同一个对象的 `b.width`。

### 坑点

- `this` 指向当前对象。
- `this->x` 常用于区分成员变量和同名形参。
- `this` 本身不能改指向。
- `return *this;` 常用于链式调用。
- 静态成员函数没有 `this` 指针。

## 11. 访问权限与友元阴招

### 考法定位

访问权限常考 `public/private/protected` 的边界，以及友元是否是成员函数。特别注意：友元可以访问私有成员，但友元函数不是成员函数，没有 `this` 指针。

### 典型题：判断哪些访问合法

```cpp
#include <iostream>
using namespace std;

class Account {
private:
    int balance;

public:
    Account(int money = 0) : balance(money) {}

    void compare(Account other) {
        cout << "other balance=" << other.balance << endl;
    }

    friend void addMoney(Account& acc, int money);
};

void addMoney(Account& acc, int money) {
    acc.balance += money;
    cout << "after add=" << acc.balance << endl;

    // 错误示范：不能通过编译
    // this->balance = 0;
}

int main() {
    Account a(100);
    Account b(200);

    a.compare(b);
    addMoney(a, 50);

    // 错误示范：不能通过编译
    // cout << a.balance << endl;

    return 0;
}
```

### 答案

```text
other balance=200
after add=150
```

### 解析

`balance` 是私有成员，类外不能通过 `a.balance` 直接访问。

`compare()` 是 `Account` 的成员函数，所以它可以访问另一个 `Account` 对象 `other` 的私有成员。

`addMoney()` 是友元函数，因此可以访问 `Account` 的私有成员。但友元函数不是成员函数，所以不能使用 `this`。

### 坑点

- `class` 默认访问权限是 `private`，`struct` 默认访问权限是 `public`。
- 类外不能直接访问 `private` 成员。
- 同一个类的成员函数可以访问同类其他对象的私有成员。
- `protected` 成员类外不能访问，派生类内部可以访问。
- 友元函数可以访问私有成员，但它不是成员函数。
- 友元关系不传递、不继承。
- `friend` 声明写在 `public` 或 `private` 区都可以。

## 12. 引用与指针传参阴招

### 考法定位

这一章常和构造、拷贝构造、输出题结合考。值传参会产生副本，引用传参不产生副本；指针传参传的是地址，修改 `*p` 会影响实参，修改 `p` 本身一般不影响外部指针。

### 典型题：写出程序输出

```cpp
#include <iostream>
using namespace std;

class Num {
private:
    int value;

public:
    Num(int v = 0) : value(v) {
        cout << "构造" << value << endl;
    }

    Num(const Num& other) : value(other.value) {
        cout << "拷贝" << value << endl;
    }

    ~Num() {
        cout << "析构" << value << endl;
    }

    void add(int n) {
        value += n;
    }

    int get() const {
        return value;
    }
};

void byValue(Num x) {
    x.add(10);
    cout << "byValue: " << x.get() << endl;
}

void byRef(Num& x) {
    x.add(20);
    cout << "byRef: " << x.get() << endl;
}

void byPtr(Num* p) {
    p->add(30);
    cout << "byPtr: " << p->get() << endl;
}

int main() {
    Num a(1);

    byValue(a);
    cout << "after byValue: " << a.get() << endl;

    byRef(a);
    cout << "after byRef: " << a.get() << endl;

    byPtr(&a);
    cout << "after byPtr: " << a.get() << endl;

    return 0;
}
```

### 答案

```text
构造1
拷贝1
byValue: 11
析构11
after byValue: 1
byRef: 21
after byRef: 21
byPtr: 51
after byPtr: 51
析构51
```

### 解析

`Num a(1)` 构造对象 `a`。

`byValue(a)` 是值传参，会调用拷贝构造，函数里修改的是副本，所以 `a` 仍然是 `1`。

`byRef(a)` 是引用传参，`x` 就是 `a` 的别名，修改会影响 `a`。

`byPtr(&a)` 是指针传参，通过 `p->add(30)` 修改的是 `a` 本身。

函数结束时，值传参产生的副本先析构；`main` 结束时，`a` 析构。

### 坑点

- 值传参会调用拷贝构造。
- 引用传参不会调用拷贝构造。
- 指针传参也不会拷贝对象本身。
- 修改引用形参会影响实参。
- 修改 `*p` 会影响实参对象；修改 `p` 本身通常不影响外部指针。
- 要修改外部指针本身，可用指针引用 `int*& p` 或二级指针。
- 非 `const` 引用不能绑定临时对象，`const` 引用可以。

## 13. 继承访问权限阴招

### 考法定位

继承访问权限考的是“基类成员到了派生类中变成什么权限”。读题时先看三件事：基类成员原本是什么权限、继承方式是什么、访问发生在类内还是类外。

### 典型题：判断访问是否合法

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    int pub;

protected:
    int pro;

private:
    int pri;
};

class PublicDerive : public Base {
public:
    void test() {
        pub = 1;
        pro = 2;

        // 错误示范：不能通过编译
        // pri = 3;
    }
};

class PrivateDerive : private Base {
public:
    void test() {
        pub = 1;
        pro = 2;

        // 错误示范：不能通过编译
        // pri = 3;
    }
};

int main() {
    PublicDerive d1;
    d1.pub = 10;

    // 错误示范：不能通过编译
    // d1.pro = 20;

    PrivateDerive d2;

    // 错误示范：不能通过编译
    // d2.pub = 30;

    return 0;
}
```

### 答案

`d1.pub = 10;` 合法。`d1.pro = 20;` 不合法。`d2.pub = 30;` 不合法。派生类内部可以访问基类的 `public` 和 `protected`，但不能直接访问基类的 `private`。

### 解析

`PublicDerive : public Base` 表示公有继承，基类的 `public` 到派生类中仍是 `public`，所以类外可以访问 `d1.pub`。

基类的 `protected` 在公有继承后仍是 `protected`，派生类内部能访问，类外不能访问。

`PrivateDerive : private Base` 表示私有继承，基类的 `public` 和 `protected` 都会变成派生类的 `private`，所以类外不能访问 `d2.pub`。

### 坑点

- `class D : B` 默认是私有继承。
- `struct D : B` 默认是公有继承。
- 基类 `private` 成员被继承了，但派生类不能直接访问。
- 公有继承保持 `public/protected` 级别。
- 保护继承会把基类 `public/protected` 都变为派生类的 `protected`。
- 私有继承会把基类 `public/protected` 都降为派生类的 `private`。
- 访问是否合法，既要看继承方式，也要看访问位置。

## 14. 继承与构造析构阴招

### 考法定位

继承中的构造析构是输出题高频点。核心规律是：构造先基类后派生类，析构先派生类后基类；如果基类没有默认构造函数，派生类必须在初始化列表中显式调用基类构造函数。

### 典型题：写出程序输出

```cpp
#include <iostream>
using namespace std;

class Base {
private:
    int x;

public:
    Base(int n) : x(n) {
        cout << "Base构造" << x << endl;
    }

    ~Base() {
        cout << "Base析构" << x << endl;
    }
};

class Member {
public:
    Member() {
        cout << "Member构造" << endl;
    }

    ~Member() {
        cout << "Member析构" << endl;
    }
};

class Derived : public Base {
private:
    Member m;

public:
    Derived(int n) : Base(n) {
        cout << "Derived构造" << endl;
    }

    ~Derived() {
        cout << "Derived析构" << endl;
    }
};

int main() {
    Derived d(5);
    return 0;
}
```

### 答案

```text
Base构造5
Member构造
Derived构造
Derived析构
Member析构
Base析构5
```

### 解析

创建 `Derived d(5)` 时，先构造基类部分，所以先调用 `Base(5)`。

然后构造成员对象 `m`，所以输出 `Member构造`。

最后执行 `Derived` 构造函数体，输出 `Derived构造`。

程序结束时析构顺序相反：先执行 `Derived` 析构函数体，再析构成员对象 `m`，最后析构基类 `Base`。

### 补充题：找错误

```cpp
class Base {
public:
    Base(int x) {}
};

class Derived : public Base {
public:
    // 错误示范：不能通过编译
    Derived() {
        // Base 没有无参构造函数，这里没有显式调用 Base(int)
    }
};
```

正确写法：

```cpp
class Base {
public:
    Base(int x) {}
};

class Derived : public Base {
public:
    Derived() : Base(10) {}
};
```

### 坑点

- 构造顺序：基类 -> 成员对象 -> 派生类构造函数体。
- 析构顺序：派生类析构函数体 -> 成员对象 -> 基类。
- 成员对象的初始化顺序看声明顺序，不看初始化列表顺序。
- 基类没有默认构造时，派生类必须显式调用基类构造。
- 派生类不会普通继承基类的构造函数和析构函数。
- 派生类对象可以隐式转成基类对象、指针或引用；基类对象不能自动转成派生类对象。

## 15. 虚函数与多态阴招

### 考法定位

虚函数常考“到底调用基类还是派生类”。判断时先看三件事：有没有继承、函数是不是 `virtual`、是不是通过基类指针或引用调用。缺一个，通常就不是运行时多态。

### 典型题：写出运行结果

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual void show() {
        cout << "Base show" << endl;
    }

    void print() {
        cout << "Base print" << endl;
    }
};

class Derived : public Base {
public:
    void show() {
        cout << "Derived show" << endl;
    }

    void print() {
        cout << "Derived print" << endl;
    }
};

int main() {
    Derived d;
    Base* p = &d;

    p->show();
    p->print();

    return 0;
}
```

### 答案

```text
Derived show
Base print
```

### 解析

`show()` 是虚函数，通过 `Base*` 指向 `Derived` 对象调用，会发生动态绑定，所以调用 `Derived::show()`。

`print()` 不是虚函数，虽然对象实际是 `Derived`，但指针类型是 `Base*`，所以调用 `Base::print()`。

### 补充题：虚函数默认参数

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual void f(int x = 1) {
        cout << "Base " << x << endl;
    }
};

class Derived : public Base {
public:
    void f(int x = 2) override {
        cout << "Derived " << x << endl;
    }
};

int main() {
    Derived d;
    Base* p = &d;
    p->f();
    return 0;
}
```

### 答案

```text
Derived 1
```

### 解析

函数体动态绑定，所以调用 `Derived::f`。默认参数静态绑定，所以默认值看 `Base*`，使用 `Base` 中的 `1`。

### 坑点

- 多态看“基类指针/引用 + virtual”。
- 普通成员函数不发生运行时多态。
- 构造函数不能是虚函数。
- 析构函数可以是虚函数，基类常常应该写虚析构。
- 静态成员函数不能是虚函数，因为它没有 `this`。
- 友元函数不能是虚函数，因为友元不是成员函数。
- 构造/析构函数中调用虚函数，通常不表现为派生类版本。

## 16. 纯虚函数与抽象类阴招

### 考法定位

纯虚函数常考“这个类能不能创建对象”。只要类中有未实现的纯虚函数，这个类就是抽象类，不能实例化，但可以定义指针或引用。

### 典型题：判断是否合法

```cpp
#include <iostream>
using namespace std;

class Shape {
public:
    virtual void draw() = 0;
};

class Circle : public Shape {
public:
    void draw() {
        cout << "Circle" << endl;
    }
};

int main() {
    // 错误示范：不能通过编译
    // Shape s;

    Circle c;
    Shape* p = &c;
    p->draw();

    return 0;
}
```

### 答案

程序合法，输出：

```text
Circle
```

### 解析

`Shape` 有纯虚函数 `draw()`，所以 `Shape` 是抽象类，不能写 `Shape s;`。

`Circle` 重写了 `draw()`，因此 `Circle` 不再是抽象类，可以创建对象。`Shape* p = &c;` 是基类指针指向派生类对象，调用虚函数时发生多态。

### 坑点

- `virtual void f() = 0;` 是纯虚函数。
- 抽象类不能创建对象，但可以定义指针和引用。
- 派生类如果没有实现全部纯虚函数，仍然是抽象类。
- 纯虚函数也可以有函数体，但类仍然是抽象类。
- 抽象类可以有构造函数，因为派生类对象中仍然包含基类子对象。

## 17. 重载、隐藏、覆盖阴招

### 考法定位

这章最容易混：重载 `overload`、隐藏 `hide`、覆盖 `override`。判断时先看作用域，再看是否 `virtual`，最后看参数表和 `const` 是否一致。

### 典型题：写出运行结果

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual void f(int x) {
        cout << "Base f(int)" << endl;
    }

    void g() {
        cout << "Base g()" << endl;
    }
};

class Derived : public Base {
public:
    void f(int x) {
        cout << "Derived f(int)" << endl;
    }

    void g(int x) {
        cout << "Derived g(int)" << endl;
    }
};

int main() {
    Derived d;
    Base* p = &d;

    p->f(1);
    p->g();

    d.g(1);
    // 错误示范：不能通过编译
    // d.g();

    return 0;
}
```

### 答案

```text
Derived f(int)
Base g()
Derived g(int)
```

### 解析

`f(int)` 在基类中是虚函数，派生类中参数一致，所以是覆盖。通过 `Base*` 调用时执行 `Derived::f(int)`。

`g()` 不是虚函数，`p->g()` 根据指针静态类型调用 `Base::g()`。

`Derived` 中定义了同名函数 `g(int)`，会隐藏基类的所有同名 `g`，所以 `d.g()` 不能直接调用。

### 坑点

- 重载：同一作用域，函数名相同，参数不同。
- 覆盖：派生类重写基类虚函数，参数表要一致。
- 隐藏：派生类出现同名函数，会隐藏基类同名函数。
- 返回值不同不能构成重载。
- `const` 不一致可能导致没有真正覆盖。
- `override` 可以帮你抓错签名。
- `using Base::f;` 可以恢复被隐藏的基类重载。

## 18. 对象切片阴招

### 考法定位

对象切片常考“派生类对象赋给基类对象后，派生类部分是否还在”。只要是按值赋给基类对象或按值传基类参数，派生类特有部分就会被切掉。

### 典型题：写出运行结果

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual void show() {
        cout << "Base show" << endl;
    }
};

class Derived : public Base {
public:
    void show() {
        cout << "Derived show" << endl;
    }
};

void test(Base b) {
    b.show();
}

int main() {
    Derived d;

    Base b = d;
    b.show();

    test(d);

    Base& r = d;
    r.show();

    return 0;
}
```

### 答案

```text
Base show
Base show
Derived show
```

### 解析

`Base b = d;` 是用派生类对象初始化基类对象，发生对象切片，`b` 里面只剩下 `Base` 部分，所以 `b.show()` 调用 `Base::show()`。

`test(d)` 是按值传参，形参类型是 `Base`，也会切片，所以输出 `Base show`。

`Base& r = d;` 是引用绑定，不会切片，并且 `show()` 是虚函数，所以输出 `Derived show`。

### 坑点

- 按值存基类对象会切片。
- 按值传基类参数会切片。
- 容器存基类对象也会切片，例如 `vector<Base>` 存 `Derived`。
- 基类指针和引用不会切片。
- 多态对象尽量用指针或引用，不要按值传递。

## 19. 运算符重载阴招

### 考法定位

运算符重载常考两类：一类是“能不能重载”，另一类是“应该写成成员还是友元”。重点记住不能改变运算符原有规则，且有些运算符必须写成成员函数。

### 典型题：判断并写输出

```cpp
#include <iostream>
using namespace std;

class Point {
private:
    int x, y;

public:
    Point(int a = 0, int b = 0) : x(a), y(b) {}

    Point operator+(const Point& other) const {
        return Point(x + other.x, y + other.y);
    }

    Point& operator+=(const Point& other) {
        x += other.x;
        y += other.y;
        return *this;
    }

    friend ostream& operator<<(ostream& out, const Point& p) {
        out << "(" << p.x << "," << p.y << ")";
        return out;
    }
};

int main() {
    Point p1(1, 2), p2(3, 4);

    Point p3 = p1 + p2;
    cout << p3 << endl;

    p1 += p2;
    cout << p1 << endl;

    return 0;
}
```

### 答案

```text
(4,6)
(4,6)
```

### 解析

`operator+` 通常返回一个新对象，所以 `p1 + p2` 得到新的 `Point(4,6)`。

`operator+=` 通常修改当前对象，并返回 `*this` 的引用，所以 `p1 += p2` 后，`p1` 自身变成 `(4,6)`。

`operator<<` 左操作数是 `ostream`，所以常写成友元非成员函数。

### 坑点

- 不能重载不存在的运算符。
- 不能改变优先级、结合性和操作数个数。
- 至少一个操作数必须是自定义类型，不能重载 `int + int`。
- `.`, `.*`, `::`, `?:`, `sizeof` 不能重载。
- `operator=`, `operator[]`, `operator()`, `operator->` 必须是成员函数。
- `operator&&`, `operator||` 重载后不保证短路。
- 重载 `new/delete` 不等于构造/析构。

## 20. 类型转换阴招

### 考法定位

类型转换常考“能不能隐式转换”和“该用哪种 cast”。类中单参数构造函数可能触发隐式转换，`explicit` 可以阻止这种转换。

### 典型题：判断是否合法

```cpp
#include <iostream>
using namespace std;

class Number {
private:
    int value;

public:
    explicit Number(int v) : value(v) {}

    operator int() const {
        return value;
    }
};

int main() {
    // 错误示范：不能通过编译
    // Number n1 = 10;

    Number n2(10);
    int x = n2;

    cout << x << endl;

    return 0;
}
```

### 答案

```text
10
```

### 解析

`Number(int)` 被 `explicit` 修饰，因此不能使用 `Number n1 = 10;` 这种隐式转换写法。

`Number n2(10);` 是直接初始化，合法。

`operator int() const` 是类型转换函数，可以把 `Number` 对象转换成 `int`，所以 `int x = n2;` 合法。

### 坑点

- 派生类到基类是安全的隐式转换。
- 基类到派生类不能自动转换。
- `static_cast` 向下转型不做运行时检查。
- `dynamic_cast` 主要用于多态类型的安全向下转型。
- `dynamic_cast` 指针失败返回 `nullptr`，引用失败抛异常。
- `const_cast` 去掉 `const` 后，如果修改真正的 `const` 对象，行为危险。
- 单参数构造函数可能产生隐式类型转换。
- `explicit` 禁止隐式转换，但不禁止直接初始化。
- 类型转换函数写法是 `operator 类型()`，没有返回类型。

## 21. 常见判断题秒杀表

### 考法定位

判断题常喜欢把“可以”和“必须”、“属于对象”和“属于类”、“初始化”和“赋值”混在一起。做题时先找绝对化词语，再看是否违反基本语法规则。

### 典型题：判断正误

| 说法 | 答案 | 解析 |
| --- | --- | --- |
| 构造函数可以有返回值。 | 错 | 构造函数没有返回类型，连 `void` 也不能写。 |
| 构造函数可以重载。 | 对 | 参数表不同即可。 |
| 构造函数可以有默认参数。 | 对 | 但要小心二义性。 |
| 构造函数可以是虚函数。 | 错 | 构造时对象尚未完整形成，不能 `virtual`。 |
| 构造函数可以是 `const` 成员函数。 | 错 | `A() const` 非法。 |
| 析构函数可以是虚函数。 | 对 | 基类析构常应写成 `virtual`。 |
| 析构函数可以重载。 | 错 | 析构函数不能带参数。 |
| 静态成员函数有 `this` 指针。 | 错 | `static` 属于类，不属于某个对象。 |
| 静态成员函数可以直接访问普通成员。 | 错 | 必须通过对象访问。 |
| 静态成员函数可以是虚函数。 | 错 | 虚函数依赖对象和 `this`。 |
| `const` 对象可以调用非 `const` 成员函数。 | 错 | `const` 对象只能调用 `const` 成员函数。 |
| `const` 成员函数一定不能改任何东西。 | 错 | 可改 `mutable` 成员或静态成员。 |
| `private` 成员不能被类外直接访问。 | 对 | 需通过 `public` 接口或友元访问。 |
| 派生类不能继承基类 `private` 成员。 | 错 | 继承了，但派生类不能直接访问。 |
| `class` 默认 `public`。 | 错 | `class` 默认 `private`。 |
| `struct` 默认 `public`。 | 对 | 包括成员和继承。 |
| 友元函数是成员函数。 | 错 | 友元没有 `this`。 |
| 友元关系可以传递。 | 错 | 友元不传递。 |
| 友元关系可以继承。 | 错 | 友元不继承。 |
| 返回局部变量引用是安全的。 | 错 | 函数结束后局部变量已销毁。 |
| 引用传参会拷贝对象。 | 错 | 引用传参不拷贝。 |
| 值传参会拷贝对象。 | 对 | 类对象会调用拷贝构造。 |
| 成员初始化顺序看初始化列表顺序。 | 错 | 实际看成员声明顺序。 |
| 派生类对象赋给基类对象会切片。 | 对 | 派生部分丢失。 |
| 基类指针指向派生类对象一定多态。 | 错 | 还需要虚函数。 |
| 纯虚函数可以有函数体。 | 对 | 类外可定义。 |
| 抽象类不能定义指针。 | 错 | 不能实例化对象，但可定义指针/引用。 |
| 返回值不同可以函数重载。 | 错 | 仅返回值不同不行。 |
| 派生类同名函数一定覆盖基类函数。 | 错 | 可能只是隐藏。 |
| 运算符重载能改变优先级。 | 错 | 不能。 |
| `.` 可以重载。 | 错 | 不能。 |
| `operator=` 必须是成员函数。 | 对 | 高频。 |
| `operator<<` 通常写成友元非成员函数。 | 对 | 左操作数是 `ostream`。 |

### 坑点

- “不能访问”不等于“没有继承”。
- “不能实例化”不等于“不能定义指针”。
- “没有返回类型”不等于“返回 `void`”。
- “引用不拷贝”不等于“对象不会被修改”。

## 22. 高频小题模板

### 考法定位

这部分适合考前刷题。遇到输出题，先数对象；遇到语法题，先找构造、析构、`static`、`const`、`virtual` 这些关键字。

### 模板 1：构造析构输出

```cpp
#include <iostream>
using namespace std;

class A {
public:
    A() {
        cout << "A()" << endl;
    }

    A(const A& other) {
        cout << "copy A" << endl;
    }

    ~A() {
        cout << "~A()" << endl;
    }
};

void f(A x) {
    cout << "f" << endl;
}

int main() {
    A a;
    f(a);
    cout << "end" << endl;
    return 0;
}
```

答案：

```text
A()
copy A
f
~A()
end
~A()
```

解析：`A a;` 调用默认构造。`f(a)` 是值传参，调用拷贝构造生成形参 `x`。函数结束时 `x` 析构。最后 `main` 结束，`a` 析构。

### 模板 2：static 与 this

```cpp
class A {
private:
    int x;
    static int count;

public:
    static void f() {
        // 错误示范：不能通过编译
        // x = 1;

        // 错误示范：不能通过编译
        // this->x = 1;

        count++;
    }
};

int A::count = 0;
```

答案：`count++` 合法，直接访问 `x` 或 `this->x` 不合法。

解析：静态成员函数属于类，不绑定具体对象，因此没有 `this` 指针。普通成员 `x` 必须依赖某个对象存在，所以不能在 `static` 函数中直接访问。

### 模板 3：虚析构

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual ~Base() {
        cout << "~Base" << endl;
    }
};

class Derived : public Base {
public:
    ~Derived() {
        cout << "~Derived" << endl;
    }
};

int main() {
    Base* p = new Derived;
    delete p;
    return 0;
}
```

答案：

```text
~Derived
~Base
```

解析：`Base` 的析构函数是虚函数，通过基类指针删除派生类对象时，会先调用派生类析构，再调用基类析构。

### 模板 4：成员初始化顺序

```cpp
class A {
    int x;
    int y;

public:
    A() : y(1), x(y + 1) {}
};
```

答案：这段代码的 `x` 初始化不可靠。因为先声明 `x`，所以先初始化 `x`；此时 `y` 还没有初始化。

### 模板 5：虚函数默认参数

```cpp
Base* p = new Derived;
p->f();
```

答案：若 `f` 是虚函数，函数体看实际对象；默认参数看指针静态类型。

## 23. 一页口诀

### 考法定位

最后一页用于考前快速过脑。口诀不是替代理解，而是帮助你在选择题和判断题中快速排除错误选项。

### 关键词反应表

| 关键词 | 立刻想到 |
| --- | --- |
| 构造函数 | 同名、无返回、可重载、可默认参数、不能 `virtual`、不能 `const` |
| 析构函数 | `~类名`、无参数、不能重载、可以 `virtual` |
| 拷贝构造 | 用旧对象初始化新对象，常写 `const A&` |
| 赋值运算符 | 已有对象之间赋值，不是拷贝构造 |
| 初始化列表 | `const`、引用、无默认构造成员、基类有参构造 |
| 初始化顺序 | 看声明顺序，不看初始化列表顺序 |
| 值传参 | 拷贝一份 |
| 引用传参 | 不拷贝，可能改实参 |
| `static` | 属于类，无 `this` |
| `const` 成员函数 | 不改普通成员，`const` 对象只能调 `const` 函数 |
| `virtual` | 基类指针/引用调用才体现多态 |
| 纯虚函数 | `=0`，抽象类不能实例化 |
| 对象切片 | 派生类按值变基类，派生部分丢失 |
| `private` | 类外不能直接访问，但不代表没继承 |
| 友元 | 不是成员，无 `this`，可访问私有 |
| `explicit` | 禁止隐式转换 |
| `operator` | 不能改优先级、结合性、操作数个数 |

### 考前短句

```text
构造不返回，析构不带参。
构造不能虚，析构可以虚。
值传参会拷贝，引用传参不拷贝。
先构造的后析构，后构造的先析构。
成员初始化看声明，不看列表。
static 无 this，const 不乱改。
父指针删子对象，父析构要 virtual。
有纯虚就是抽象类，抽象类不能造对象。
同名不一定覆盖，参数不对就是隐藏。
多态对象别按值传，按值传就会切片。
```

### 最后提醒

- 口诀要配合题目语境，尤其注意“现代编译器可能进行拷贝省略”。
- 如果试题说明“不考虑优化”，按传统模型数拷贝构造。
- 如果试题给的是错误代码，先判断能不能编译，再谈运行结果。
