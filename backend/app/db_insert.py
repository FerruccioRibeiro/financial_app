import sqlite3
from dateutil.relativedelta import relativedelta
from datetime import datetime


# Funcao insert output hist
def insert_or_update_output_hist(category, init_month, sum_value, cur, conn):

    # Confere se ja existe na tabela output_hist
    cur.execute(f"SELECT value FROM output_hist WHERE is_delete = 0 AND date = '{init_month}' AND category = '{category}' ")
    result = cur.fetchall()

    # Insert nas tabelas output_hist
    if result == []:
        cur.execute("""
            INSERT INTO output_hist (category, value, date)
            VALUES (?, ?, ?)
        """, (category, sum_value, init_month))
        conn.commit()
        fk_oh = cur.lastrowid
    else:
        sum_total = result[0][0]
        cur.execute(f"""
            SELECT 
                pk_oh 
            FROM output_hist 
            WHERE 
                is_delete = 0 
                AND date = '{init_month}' 
                AND category = '{category}' 
        """)
        fk_oh = cur.fetchall()[0][0]

        cur.execute(f"""
            UPDATE output_hist 
            SET value = {sum_total + sum_value}
            WHERE 
                is_delete = 0 
                AND pk_oh = {fk_oh}
        """)
        conn.commit()
    
    return fk_oh

# Funcao insert purchase installments
def insert_purchase_installments(fk_oh, category, sum_value, description, date, init_month, bank, location, installments, payment_m, cur, conn):
    # Insere na tabela de compra
    cur.execute(f"SELECT MAX(pk_purch_inst) FROM purchases_installments  WHERE is_delete = 0 ")
    result = cur.fetchall()
    if result[0][0] == None:
        pk_purch_inst = 0
    else:
        pk_purch_inst = int(str(result[0][0])[0])

    if payment_m == "Debito":
        cur.execute("""
            INSERT INTO purchases_installments 
            (pk_purch_inst, fk_oh, description, value, category, installments, date, p_month, bank, payment_method, localization) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pk_purch_inst+1,
            fk_oh,
            description,
            sum_value,
            category,
            installments,
            date,
            init_month,
            bank,
            payment_m,
            location
        ))
        conn.commit()
    else:
        for i in range(installments):
            cur.execute("""
                INSERT INTO purchases_installments 
                (pk_purch_inst, fk_oh, description, value, category, installments, date, p_month, bank, payment_method, localization) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(str(pk_purch_inst+1) + str(i+1)),
                fk_oh,
                description,
                round(sum_value/installments,2),
                category,
                i+1,
                date,
                datetime.strftime(datetime.strptime(init_month, "%Y-%m-%d") + relativedelta(months=i), "%Y-%m-%d"),
                bank,
                payment_m,
                location
            ))
            conn.commit()
    
    return int(str(cur.lastrowid)[0])

# Funcao insert purchase itens
def insert_purchase_itens(fk_purch_inst, itens, cur, conn):
    for item in itens:
        cur.execute("""
            INSERT INTO purchase_itens (fk_purch_inst, description, value)
            VALUES (?, ?, ?)
        """, (fk_purch_inst, item[0], item[1]))
        conn.commit()

# Funcao insert input fixo
def insert_input_permanent(description, value, bank, cur, conn):
    cur.execute("""
        INSERT INTO input_permanent (description, value, bank)
        VALUES (?, ?, ?)
    """, (description, value, bank))
    conn.commit()

# Funcao insert input hist
def insert_input_hist(description, value, bank, init_month, cur, conn):
    cur.execute("""
        INSERT INTO input_hist (description, value, date, bank)
        VALUES (?, ?, ?, ?)
    """, (description, value, init_month, bank))
    conn.commit()

# Funcao insert bank
def insert_bank (name, due_date, cur, conn):
    cur.execute("""
        INSERT INTO bank (name, due_day)
        VALUES (?, ?)
    """, (name, due_date))
    conn.commit()

# Funcao output permanent
def insert_output_permanent(description, category, value, bank, init_date, end_date, rate, cur, conn):
    cur.execute("""
        INSERT INTO output_permanent (description, category, value, bank, init_date, end_date, rate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (description, category, value, bank, init_date, end_date, rate))
    conn.commit()
