#understanding the table
df_sales.info()
df_sales.head()

#changing type of order, ship, due date
df_sales["sls_order_dt"] = pd.to_datetime(df_sales["sls_order_dt"].astype(str), format = "%Y%m%d", errors = "coerce")
df_sales["sls_ship_dt"] = pd.to_datetime(df_sales["sls_ship_dt"].astype(str), format= "%Y%m%d", errors = "coerce")
df_sales["sls_due_dt"] = pd.to_datetime(df_sales["sls_due_dt"].astype(str), format= "%Y%m%d", errors = "coerce")

df_sales.info()

#checking the order date is smaller than the ship date
df_sales[df_sales["sls_order_dt"] > df_sales["sls_ship_dt"]]

#checking the order date is smaller than the due date
df_sales[df_sales["sls_order_dt"] > df_sales["sls_due_dt"]]

df_sales.head()

#checking sales is equal to quantity * price
df_sales[df_sales["sls_sales"] != df_sales["sls_quantity"] * df_sales["sls_price"]]

# Calculateing the Expected Sales Value (Quantity * Absolute Price)
expected_sales = df_sales["sls_quantity"] * df_sales["sls_price"].abs()


#using 0.01 for value greater than 0 
tolerance = 0.01
cond = (
    df_sales["sls_sales"].isna() | 
    (df_sales["sls_sales"] <= 0) | 
    (abs(df_sales["sls_sales"] - expected_sales) > tolerance)
)

# appling the condition
df_sales.loc[cond, "sls_sales"] = expected_sales

#checking sales is equal to quantity * price
df_sales[df_sales["sls_sales"] != df_sales["sls_quantity"] * df_sales["sls_price"]]

#correcting the sales price column 
df_sales["sls_price"] = df_sales["sls_sales"] / df_sales["sls_quantity"]

#checking the sales price coloumn
df_sales[df_sales["sls_price"] != df_sales["sls_sales"] / df_sales["sls_quantity"]]

#Rechecking sales is equal to quantity * price
df_sales[df_sales["sls_sales"] != df_sales["sls_quantity"] * df_sales["sls_price"]]

df_sales.info()
df_sales.head()

dim_customer.head()

dim_product.head()

# ************************ Creating fact sale table ************************ 

# replacing the column sls_prd_key and sls_cust_id with dimension customer key(surrogate key) and dimension product key (surrogate key)for better joining 
fact_sales = pd.merge(df_sales, dim_product[["prd_key","prd_number"]] , left_on = "sls_prd_key", right_on = "prd_number", how = "left")

fact_sales.head()

# deleting the sls_prd_key and prd_number 
fact_sales.drop(columns = {
    "prd_number",
    "sls_prd_key"
}, inplace= True)

fact_sales.head()

# adding the cst_key column in fact_sles
fact_sales = pd.merge(fact_sales, dim_customer[["cst_key", "cst_id"]], left_on = "sls_cust_id", right_on = "cst_id", how = "left")

fact_sales.head()

# dropning the cst_id and sls_cust_id column 
fact_sales.drop(columns = {
    "sls_cust_id",
    "cst_id"
},inplace = True)

fact_sales.head()

# ************************ saving fact sales in csv form ************************ 

fact_sales.to_csv("clean_fact_sales.csv", index = False)










