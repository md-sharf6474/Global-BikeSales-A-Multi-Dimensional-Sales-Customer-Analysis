
#*****************  CLEANING THE CUSTOMER INFORMATION TABLE *******************

df_cust_info.isnull().sum()
df_cust_info.info()
df_cust_info.head()

## converting cst_create_date to datetime 
df_cust_info["cst_create_date"] = pd.to_datetime(df_cust_info["cst_create_date"], format = "mixed", errors = "coerce")
df_cust_info["cst_create_date"].info()
df_cust_info["cst_create_date"].head()

# droping null in primary key
df_cust_info = df_cust_info.dropna(subset = ["cst_id"])
df_cust_info.isnull().sum()

# checking repeated values in primary key 
df_cust_info["cst_id"].value_counts()[df_cust_info["cst_id"].value_counts() > 1]

# keeping one with new date 
df_cust_info = df_cust_info.sort_values(["cst_id","cst_create_date"],ascending = [True,False]).drop_duplicates(subset = "cst_id", keep = "first")

#changing the type of cst_id to integer
df_cust_info["cst_id"] = df_cust_info["cst_id"].astype(int)

# checking extra spaces in firstname 
df_cust_info[df_cust_info["cst_firstname"] != df_cust_info["cst_firstname"].str.strip() ]

# removing extra spaces in firstname
df_cust_info.cst_firstname = df_cust_info["cst_firstname"].str.strip()

#checking extra spaces in lastname
df_cust_info[df_cust_info["cst_lastname"] != df_cust_info["cst_lastname"].str.strip() ]

# Removing the extra spaces 
df_cust_info.cst_lastname = df_cust_info["cst_lastname"].str.strip()

# Checking extra spaces in gender
df_cust-info[df_cust_info["cst_gndr"] != df_cust_info["cst_gndr"].str.strip()]

#checking unique values
df_cust_info["cst_gndr"].unique()

# how many null in gender
df_cust_info["cst_gndr"].isnull().sum()

# counting all values
df_cust_info["cst_gndr"].value_counts(dropna = False)

# filling the null and writing full form of m and f
df_cust_info.cst_gndr = df_cust_info["cst_gndr"].str.lower()

df_cust_info.cst_gndr = df_cust_info["cst_gndr"].replace({
    "m" : "Male",
    "f" : "Female"
})
df_cust_info.cst_gndr = df_cust_info["cst_gndr"].fillna("n/a")

# checking cst_marital_status 
df_cust_info.cst_marital_status.unique()

# writing the full name of m and s in marital status
df_cust_info.cst_marital_status = df_cust_info["cst_marital_status"].str.lower()
df_cust_info.cst_marital_status = df_cust_info["cst_marital_status"].replace({
    "m" : "Married",
    "s" : "Single"
})

#************************ CLEANING THE DF_CUST_LOC TABLE ************************ 

# understanding the table 
df_cust_loc.info()
df_cust_loc.head()

# checking customer id is unique
df_cust_loc["CID"].value_counts()[df_cust_loc["CID"].value_counts() > 1 ]

#removing the underscore(_) in CID 
df_cust_loc['CID'] = df_cust_loc['CID'].str.replace('-', '', regex=False)

# checking nulls in cntry 
df_cust_loc["CNTRY"].isnull().sum()
df_cust_loc["CNTRY"].value_counts(dropna = False)

# correcting country name and filling the null
df_cust_loc["CNTRY"] = df_cust_loc["CNTRY"].str.lower()

df_cust_loc["CNTRY"] = df_cust_loc["CNTRY"].replace({
    "usa" : "united states",
    "us" : "united states",
    "de" : "germany"
})

df_cust_loc["CNTRY"] = df_cust_loc["CNTRY"].fillna("n/a")

# converting empty string into nan
df_cust_loc['CNTRY'] = df_cust_loc['CNTRY'].replace(r'^\s*$', np.nan, regex=True)

# filling nan values in country
df_cust_loc["CNTRY"] = df_cust_loc["CNTRY"].fillna("n/a")

# changing first alphabet capital
df_cust_loc.CNTRY = df_cust_loc["CNTRY"].str.title()

# changing column names 
df_cust_loc.rename(columns = {
    "CID" : "cst_key",
    "CNTRY" : "cst_country"
} , inplace = True)

##************************  CLEANING CUSTOMER DEMO TABLE ************************ 

# understanding the cust_demo table 
df_cust_demo.info()
df_cust_demo.head()

# first changing the column name 
df_cust_demo.rename( columns = {
    "CID" : "cst_key",
    "BDATE" : "birth_date",
    "GEN" : "cst_gender"
}, inplace = True)

# checking primary key is unique
df_cust_demo["cst_key"].value_counts()[df_cust_demo["cst_key"].value_counts() > 1]

# Removing the first 3 letter in cst_id for easy to join to df_cust_info
df_cust_demo.cst_key = df_cust_demo["cst_key"].replace(r"^NAS","",regex = True)

# changing birth-date to datetime 
df_cust_demo.birth_date = pd.to_datetime(df_cust_demo["birth_date"],format = "mixed", errors = "coerce")

# checking extra spaces in gender 
df_cust_demo[df_cust_demo.cst_gender != df_cust_demo["cst_gender"].str.strip()]
#counting nulls and values
df_cust_demo["cst_gender"].value_counts(dropna= False)

# removing extra spaces and converting into lower
df_cust_demo.cst_gender = df_cust_demo["cst_gender"].str.strip().str.lower()

# removing empty string with n/a 
df_cust_demo["cst_gender"] = df_cust_demo['cst_gender'].replace(r'^\s*$', np.nan, regex=True)

# writing the ful form of m and f
df_cust_demo.cst_gender = df_cust_demo["cst_gender"].replace({
    "m" : "male",
    "f" : "female"
})

# filling the null value with n/a
df_cust_demo["cst_gender"] = df_cust_demo["cst_gender"].fillna("n/a")

# making first lettter capital
df_cust_demo.cst_gender = df_cust_demo["cst_gender"].str.title()


#************************ MERGING THE CUSTOMER TABLES INTO ONE dim_customer ************************ 

#merging cust_info and cust_loc
df_merge_cust = pd.merge(df_cust_info,df_cust_loc, on = "cst_key",how = "left")

# final merging with demo table
dim_customer = pd.merge(df_merge_cust, df_cust_demo, on = "cst_key", how = "left")

#************************  REMOVING EXTRA GENDER COLUMN ************************ 
# selecting better gender column 
dim_customer["cst_gndr"].value_counts()

dim_customer["cst_gender"].value_counts()

##************************ CREATING A NEW COLUMN BY FILLING N/A VALUES IN MAIN TABLE GENDER  USING CRM GENDER COLUMN ************************ 

# FILLING N/A VALUES WITH ERP customer table 
dim_customer['final_gender'] = dim_customer.apply(
    lambda x: x['cst_gender'] if x['cst_gndr'] == 'n/a' else x['cst_gndr'],
    axis=1
)

dim_customer["final_gender"].value_counts()

# droping both gender columns 
dim_customer.drop(["cst_gndr","cst_gender"], axis = 1 , inplace = True)

#changing the column name 
dim_customer.rename(columns = ({
    "final_gender": "cst_gender",
    "birth_date" : "cst_birthdate",
    "cst_key" : "cst_number"
}),inplace = True)

dim_customer.head()

# adding surrogate key in dim_customer 
dim_customer["cst_key"] = range(1, len(dim_customer) +1)

#checking the surrogate key 
dim_customer.info()
dim_customer.tail()

## ************************ Saving dim_customer to csv file ************************ 

dim_customer.to_csv("clean_dim_customer.csv", index= False )




