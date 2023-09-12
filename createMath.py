import itertools 

# 计算后的最大结果
max_num = 100
min_num = 10
# 计算次数
calc_step = 1
# 计算类型
#calc_type = {'+', '-', '*', '/'}
#calc_type = {'+', '-'}
calc_type = {'*', '/'}

def generate_expressions(numbers, operators, depth, current_depth=1):
    if current_depth == depth:
        for num1, num2, op in itertools.product(numbers, numbers, operators):
            yield f"{num1} {op} {num2}"
    else:
        for num, sub_expression, op in itertools.product(numbers, generate_expressions(numbers, operators, depth, current_depth + 1), operators):
            yield f"{num} {op} {sub_expression}"

def is_valid_expression(expression, max_num):
    try:
        result = eval(expression)
        return result > min_num and result < max_num and isinstance(result, int)
    except (ValueError, ZeroDivisionError):
        return False

# 根据 calc_step 生成表达式
for expression in generate_expressions(range(0, max_num), calc_type, calc_step):
    if is_valid_expression(expression, max_num):
        print(expression)
