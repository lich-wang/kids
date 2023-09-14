import itertools
import random
import openpyxl

def generate_expressions(numbers, operators, depth, max_expr_count, max_num, min_num):
    numbers = list(numbers)
    random.shuffle(numbers)
    #print(f"Generating expressions with depth {depth},{max_expr_count}")
    valid_count = 0
    if depth == 0:
        return
    if depth == 1:
        for _ in range(max_expr_count):
            expression = f"{random.choice(numbers)} {random.choice(operators)} {random.choice(numbers)}"
            #print(expression,valid_count)
            try:
                result = eval(expression)
                if min_num < result < max_num and result == int(result):
                    yield expression
                    print(expression,valid_count)
                    valid_count += 1
                    if valid_count >= max_expr_count:
                        return
            except (ValueError, ZeroDivisionError):
                pass

    if depth > 1:
        print(f"Depth: {depth}")
        for _ in range(max_expr_count):
            sub_expression = next(generate_expressions(numbers, operators, depth-1, max_expr_count, max_num, min_num))
            expression = f"{random.choice(numbers)} {random.choice(operators)} {sub_expression}"
            try:
                result = eval(expression)
                if min_num < result < max_num and result == int(result):
                    yield expression
                    valid_count += 1
                    if valid_count >= max_expr_count:
                        return
            except (ValueError, ZeroDivisionError):
                pass

def generate_and_save_expressions(max_num, min_num, calc_step, calc_type, file_name, max_valid_count, start):
    print(calc_step)
    expressions = list(generate_expressions(range(start, max_num), calc_type, calc_step, max_valid_count, max_num, min_num))
    random.shuffle(expressions)  # 打乱表达式的顺序

    # 创建一个新的Excel工作簿和工作表
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # 添加表头
    worksheet.append(['Expression'])

    # 将有效表达式写入Excel
    for expression in expressions:
        expression_with_symbols = expression.replace('*', '✖').replace('/', '➗').replace('+', '➕').replace('-', '➖')
        print(expression_with_symbols)
        worksheet.append([expression_with_symbols])

    # 保存Excel文件
    workbook.save(file_name)
    print(f'{len(expressions)} valid expressions generated and saved to {file_name}')

max_num = 100
min_num = 10
calc_step = 1
calc_type = ['*', '/']
file_name = 'expressions.xlsx'
max_valid_count = 10  # 设置最大有效表达式数量

# 调用函数并指定文件名和最大有效表达式数量
generate_and_save_expressions(100, min_num, 1, calc_type, "100以内乘除.xlsx", 1000, 0)
generate_and_save_expressions(1000, 100, 2, ['+', '-'], "1000以内连加连减.xlsx", 60000, 100)
