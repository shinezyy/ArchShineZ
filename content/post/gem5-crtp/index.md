---
title: 在GEM5中用到的两个C++模板知识
subtitle: 

# Summary for listings and search engines
summary: 在GEM5中用到的两个C++模板知识

# Link this post with a project
projects: []

# Date published
date: "2021-03-01T00:00:00Z"

# Date updated
lastmod: "2021-03-01T00:00:00Z"

# Is this an unpublished draft?
draft: false

# Show this page in the Featured widget?
featured: false

# Featured image
# Place an image named `featured.jpg/png` in this page's folder and customize its options here.
image:
  caption: 'Image credit: [**GEM5**](https://gem5.org/)'
  focal_point: ""
  placement: 2
  preview_only: false

authors:
- admin

tags:
- Architecture
- GEM5

categories:
- 工作
---

# 在GEM5中用到的两个C++模板知识



GEM5的O3用了模板，stl helper也用了模板，这两部分的模板知识可能在本科的C++课程中没有讲到，这里做一个导航，推荐一些相关的讨论和文章。因为我不是很懂PL，讲错了还请直接在评论区指出。

## O3的CRTP

第一部分是O3里面的[CRTP (Curiously recurring template pattern)](https://en.wikipedia.org/wiki/Curiously_recurring_template_pattern)，可以看这个问题下面的第二个答案：[Confusion about CRTP static polymorphism](https://stackoverflow.com/questions/43821541/confusion-about-crtp-static-polymorphism)，和这篇文章[Design Patterns With C++（八）CRTP（上）](https://zhuanlan.zhihu.com/p/142407249)

在GEM5 O3里面用CRTP来替代动态多态有两个好处：

1. CRTP是编译期的，所以没有运行时的虚函数带来的开销。不难理解，对于C++写的模拟器而言性能是十分重要的。
2. CRTP可以控制基类调用派生类的方法。

如果看不懂也没关系，因为我最开始也看不懂，现在也还玩不转CRTP。下面讲一讲CRTP在GEM5  O3里面照猫画虎的用法：以O3的Fetch为例。现在GEM5已经实现了一个DefaultFetch，假设你再实现了一个FancyFetch。只要FancyFetch的接口和DefaultFetch完全一样，你就可以在`cpu_policy.hh`中把` typedef DefaultFetch<Impl> Fetch`替换成` typedef FancyFetch<Impl> Fetch`。 这样Fetch流水级会就使用你实现的FancyFetch来取值了。

## STL helper的printer重载歧义

第二部分是`src/base/stl_helpers.hh`里面的`ContainerPrinter `。在C++17中，GEM5为Container重载的ostream<< 会和`std::basic_string` 的 << 产生歧义。如果你现在把GEM5改为C++17的标准，大概率是编译不过的。我们需要对重载进行更严格的限制。

为了解决这个问题，我主要学习了这个[关于Generic Printer的讨论](https://stackoverflow.com/questions/51531514/c-print-template-container-error-error-ambiguous-overload-for-operator/51532253)，下面的内容是对这个讨论的简单解释。

第一层，最naive的Generic Printer长这样：

```cpp
template<typename Container>
std::ostream& operator<<(std::ostream& out, const Container& c){
    for(auto item:c){
        out<<item;
    }
    return out;
}
```

写成这样的肯定会报错：`error: ambiguous overload for 'operator<<'`，因为和基本类型冲突了。

第二层，针对Container的Generic Printer：

```cpp
template<typename T, template <typename, typename> class Container>
std::ostream& operator<<(std::ostream& out, const Container<T, std::allocator<T>>& c) {
    for (auto item : c) {
        out << item << " ";
    } 
    return out;
}
```

GEM5就采用了这种写法，这么写避免了和基本类型冲突。因为它约束了Container这个模板类的pattern：必须有 `T`和 `std::allocator<T>`两个模板参数。 但是这么写的问题就是`std::basic_string`也长这样。

第二层，屏蔽掉的std::basic_string派生类的Generic Printer：

```cpp
template<template<typename...> typename From, typename T>
struct is_from : std::false_type {};

template<template<typename...> typename From, typename ... Ts>
struct is_from<From, From<Ts...> > : std::true_type {};

template <typename...>
using void_t = void;

template <typename T, typename = void>
struct is_input_iterator : std::false_type { };

template <typename T>
struct is_input_iterator<T,
    void_t<decltype(++std::declval<T&>()),
           decltype(*std::declval<T&>()),
           decltype(std::declval<T&>() == std::declval<T&>())>>
    : std::true_type { };

template<typename Container, 
typename std::enable_if<is_input_iterator<decltype(std::begin(std::declval<Container>()))>::value &&
                        is_input_iterator<decltype(std::end(std::declval<Container>()))>::value &&
                        !is_from<std::basic_string, Container>::value, int>::type = 0>
std::ostream& operator<<(std::ostream& out, const Container& c){
    for(const auto& item:c){
        out << item << " ";
    }
    return out;
}
```

这个写法用[sfinae](https://en.cppreference.com/w/cpp/language/sfinae)进一步约束的两个方面：

1. 只有当Container有begin和end方法，且begin和end返回的是迭代器 (`is_input_iterator`) 时，才可以进行模板替换。什么是迭代器呢？要求有`++x`, `*x`, 和`==`方法。
2. 当Container是 `std::basic_string`的派生类的时候才能进行模板替换。

如果你想在GEM5中用C++17，遇到了上述问题，可以直接拿下面的代码去替换：

```cpp
#if (defined(__cplusplus) && __cplusplus >= 201703L) || (defined(_MSC_VER) && _MSC_VER >1900 && defined(_HAS_CXX17) && _HAS_CXX17 == 1)

template<template<typename...> typename From, typename T>
struct is_from : std::false_type {};

template<template<typename...> typename From, typename ... Ts>
struct is_from<From, From<Ts...> > : std::true_type {};

template <typename...>
using void_t = void;

template <typename T, typename = void>
struct is_input_iterator : std::false_type { };

template <typename T>
struct is_input_iterator<T,
    void_t<decltype(++std::declval<T&>()),
    decltype(*std::declval<T&>()),
    decltype(std::declval<T&>() == std::declval<T&>())>>
    : std::true_type { };

template<typename Container,
    typename std::enable_if<is_input_iterator<decltype(std::begin(std::declval<Container>()))>::value &&
    is_input_iterator<decltype(std::end(std::declval<Container>()))>::value &&
    !is_from<std::basic_string, Container>::value, int>::type = 0>
    std::ostream& operator<<(std::ostream& out, const Container& vec)
{
    out << "[ ";
    std::for_each(vec.begin(), vec.end(), ContainerPrint<decltype(*vec.begin())>(out));
    out << " ]";
    out << std::flush;
    return out;
}
#else

template <template <typename T, typename A> class C, typename T, typename A>
    std::ostream &
operator<<(std::ostream& out, const C<T,A> &vec)
{
    out << "[ ";
    std::for_each(vec.begin(), vec.end(), ContainerPrint<T>(out));
    out << " ]";
    out << std::flush;
    return out;
}
#endif
```



