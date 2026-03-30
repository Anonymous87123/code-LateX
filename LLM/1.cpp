#include <iostream>
#include <cstring>
using namespace std;

class STR {
private:
    char* p; // 存储字符串的动态数组
public:
    // 1. 构造函数：用字符串s初始化p
    STR(char* s) {
        int len = strlen(s);
        p = new char[len + 1]; // 分配动态内存（+1存结束符）
        strcpy(p, s);
    }

    // 2. 辅助函数：交换两个字符的位置
    void movechar(char& a, char& b) {
        char temp = a;
        a = b;
        b = temp;
    }

    // 3. 核心处理函数：数字移到后半部分，非数字移到前半部分
    void fun() {
        int len = strlen(p);
        int nonDigitIdx = 0; // 记录非数字字符应放置的位置

        // 遍历字符串，将非数字字符依次前移
        for (int i = 0; i < len; ++i) {
            if (!isdigit(p[i])) { // 判断非数字字符
                // 交换当前非数字字符与nonDigitIdx位置的字符
                movechar(p[i], p[nonDigitIdx]);
                nonDigitIdx++;
            }
        }
    }

    // 4. 析构函数：释放动态内存
    ~STR() {
        delete[] p;
    }

    // 5. 输出字符串
    void print() {
        cout << p << endl;
    }
};

int main() {
    char input[100];
    // 循环读取输入（处理多组输入）
    while (cin.getline(input, 100)) {
        STR s(input); // 创建STR对象
        s.fun();      // 处理字符串
        s.print();    // 输出结果
    }
    return 0;
}