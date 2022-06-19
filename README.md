## Lox interpreter

Last year in a coding contest, we were presented with the task of building an interpreter for a language resembling basic. We managed to parse strings into tokens and perform basic operations based on instructions, but the problem arose when we were asked to build nested if statements, so we decided to learn how to build an interpreter.

We found two good resources for building an interpreter, [one](https://www.youtube.com/watch?v=Eythq9848Fg&list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD&index=4&ab_channel=CodePulse) is for basic interpreter in python, and the [second](https://craftinginterpreters.com/) for lox interpreter in java and C. We are going to combine these examples and build an interpreter for lox in python.

We are going to start with basic mathematical operations, and we are going to use a simplified version of lox syntax:

```console
expression -> literal | unary | binary | grouping;
literal -> NUMBER;
grouping -> "(" expression ")";
unary -> "-" expression;
binary -> expression operator expression;
operator -> "+" | "-" | "*" | "/";
```

