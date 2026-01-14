import sqlite3


def read_month_input_hist(date, cur):
    cur.execute(f"""
        SELECT 
            pk_ih, description, value, date, bank
        FROM input_hist AS d 
        WHERE d.date = '{date}' AND d.is_delete = 0 """)
    result = cur.fetchall()
    return result

def read_input_permanent(cur):
    cur.execute(f"""
        SELECT 
            pk_ip, description, value, bank
        FROM input_permanent AS d 
        WHERE d.is_delete = 0 """)
    result = cur.fetchall()
    return result

def read_month_output_hist(date, cur):
    cur.execute(f"""
        SELECT 
            pk_oh, category, value, date
        FROM output_hist AS d 
        WHERE d.date = '{date}' AND d.is_delete = 0 """)
    result = cur.fetchall()
    return result

def read_output_permanent(cur):
    cur.execute(f"""
        SELECT 
            pk_op, description, category, value, bank, init_date, end_date, rate
        FROM output_permanent AS d 
        WHERE d.is_delete = 0 """)
    result = cur.fetchall()
    return result

def read_purchase_itens(fk_purch_inst, cur):
    cur.execute(f"""
        SELECT 
            pk_pi, fk_purch_inst, description, value
        FROM purchase_itens AS d 
        WHERE fk_purch_inst = {fk_purch_inst} AND d.is_delete = 0 """)
    result = cur.fetchall()
    return result

def read_month_bank_purchase_installments(date, bank, cur):
    cur.execute(f"""
        SELECT 
            pk_purch_inst, fk_oh, description, value, category, installments, date, p_month, bank, payment_method, localization
        FROM purchases_installments AS d 
        WHERE d.p_month = '{date}' AND d.bank = '{bank}' AND d.is_delete = 0 """)
    result = cur.fetchall()
    return result

