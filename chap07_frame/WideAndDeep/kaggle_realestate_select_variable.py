import numpy as np
import pandas as pd
import tensorflow as tf

print('Loading data ...')

train = pd.read_csv('../train_2016_v2.csv')
prop = pd.read_csv('../properties_2016.csv')
sample = pd.read_csv('../sample_submission.csv')

#print("rowcount {0}".format(len(train.index)))

# print('Binding to float32')

# for c, dtype in zip(prop.columns, prop.dtypes):
#     if dtype == np.float64:
#         prop[c] = prop[c].astype(np.float32)

print('Creating training set ...')

df_train = train.merge(prop, how='left', on='parcelid')

x_train = df_train.drop(['parcelid', 'logerror', 'transactiondate', 'propertyzoningdesc', 'propertycountylandusecode'], axis=1)
y_train = df_train['logerror'].values
print(x_train.shape, y_train.shape)

train_columns = x_train.columns

#print(x_train.dtypes)
#print(dir(x_train.dtypes))

CATEGORICAL_COLUMNS = [ _name for _name, _type in x_train.dtypes.iteritems() if _type == 'object' ]
#print(CATEGORICAL_COLUMNS)
# 여기서 column을 바꾸자

CONTINUOUS_COLUMNS = [ _name for _name, _type in x_train.dtypes.iteritems() if _type != 'object' ]
#print(CONTINUOUS_COLUMNS)

LABEL_COLUMN = 'logerror'


def build_estimator(model_dir, model_type):
    """Build an estimator."""
    # Sparse base columns.

    # ['airconditioningtypeid', 'architecturalstyletypeid', 'basementsqft', 'bathroomcnt', 'bedroomcnt', 'buildingclasstypeid'
    #airconditioningtypeid = tf.contrib.layers.real_valued_column("airconditioningtypeid")
    #architecturalstyletypeid = tf.contrib.layers.real_valued_column("architecturalstyletypeid")
    basementsqft = tf.contrib.layers.real_valued_column("basementsqft")
    bathroomcnt = tf.contrib.layers.real_valued_column("bathroomcnt")
    bedroomcnt = tf.contrib.layers.real_valued_column("bedroomcnt")
    buildingclasstypeid = tf.contrib.layers.real_valued_column("buildingclasstypeid")

    # , 'buildingqualitytypeid', 'calculatedbathnbr', 'decktypeid', 'finishedfloor1squarefeet', 'calculatedfinishedsquarefeet', 'finishedsquarefeet12', 'finishedsquarefeet13',
    buildingqualitytypeid = tf.contrib.layers.real_valued_column("buildingqualitytypeid")
    calculatedbathnbr = tf.contrib.layers.real_valued_column("calculatedbathnbr")
    decktypeid = tf.contrib.layers.real_valued_column("decktypeid")
    finishedfloor1squarefeet = tf.contrib.layers.real_valued_column("finishedfloor1squarefeet")
    calculatedfinishedsquarefeet = tf.contrib.layers.real_valued_column("calculatedfinishedsquarefeet")
    finishedsquarefeet12 = tf.contrib.layers.real_valued_column("finishedsquarefeet12")
    finishedsquarefeet13 = tf.contrib.layers.real_valued_column("finishedsquarefeet13")

    # 'finishedsquarefeet15', 'finishedsquarefeet50', 'finishedsquarefeet6', 'fips', 'fireplacecnt', 'fullbathcnt', 'garagecarcnt',

    finishedsquarefeet15 = tf.contrib.layers.real_valued_column("finishedsquarefeet15")
    finishedsquarefeet50 = tf.contrib.layers.real_valued_column("finishedsquarefeet50")
    finishedsquarefeet6 = tf.contrib.layers.real_valued_column("finishedsquarefeet6")
    fips = tf.contrib.layers.real_valued_column("fips")
    fireplacecnt = tf.contrib.layers.real_valued_column("fireplacecnt")
    fullbathcnt = tf.contrib.layers.real_valued_column("fullbathcnt")
    garagecarcnt = tf.contrib.layers.real_valued_column("garagecarcnt")

    # 'garagetotalsqft', 'heatingorsystemtypeid', 'latitude', 'longitude', 'lotsizesquarefeet', 'poolcnt', 'poolsizesum', 'pooltypeid10'

    garagetotalsqft = tf.contrib.layers.real_valued_column("garagetotalsqft")
    #heatingorsystemtypeid = tf.contrib.layers.real_valued_column("heatingorsystemtypeid")
    latitude = tf.contrib.layers.real_valued_column("latitude")
    longitude = tf.contrib.layers.real_valued_column("longitude")
    lotsizesquarefeet = tf.contrib.layers.real_valued_column("lotsizesquarefeet")
    poolcnt = tf.contrib.layers.real_valued_column("poolcnt")
    garagecarcnt = tf.contrib.layers.real_valued_column("garagecarcnt")
    poolsizesum = tf.contrib.layers.real_valued_column("poolsizesum")
    pooltypeid10 = tf.contrib.layers.real_valued_column("pooltypeid10")

    # , 'pooltypeid2', 'pooltypeid7', 'propertylandusetypeid', 'rawcensustractandblock', 'regionidcity', 'regionidcounty',
    pooltypeid2 = tf.contrib.layers.real_valued_column("pooltypeid2")
    pooltypeid7 = tf.contrib.layers.real_valued_column("pooltypeid7")
    #propertylandusetypeid = tf.contrib.layers.real_valued_column("propertylandusetypeid")
    rawcensustractandblock = tf.contrib.layers.real_valued_column("rawcensustractandblock")
    regionidcity = tf.contrib.layers.real_valued_column("regionidcity")
    regionidcounty = tf.contrib.layers.real_valued_column("regionidcounty")
    regionidneighborhood = tf.contrib.layers.real_valued_column("regionidneighborhood")

    # 'regionidneighborhood', 'regionidzip', 'roomcnt', 'storytypeid', 'threequarterbathnbr', 'typeconstructiontypeid', 'unitcnt', 'yardbuildingsqft17'
    regionidneighborhood = tf.contrib.layers.real_valued_column("regionidneighborhood")
    regionidzip = tf.contrib.layers.real_valued_column("regionidzip")
    roomcnt = tf.contrib.layers.real_valued_column("roomcnt")
    #storytypeid = tf.contrib.layers.real_valued_column("storytypeid")
    threequarterbathnbr = tf.contrib.layers.real_valued_column("threequarterbathnbr")
    #typeconstructiontypeid = tf.contrib.layers.real_valued_column("typeconstructiontypeid")
    unitcnt = tf.contrib.layers.real_valued_column("unitcnt")
    yardbuildingsqft17 = tf.contrib.layers.real_valued_column("yardbuildingsqft17")
    garagecarcnt = tf.contrib.layers.real_valued_column("garagecarcnt")

    # , 'yardbuildingsqft26', 'yearbuilt', 'numberofstories', 'structuretaxvaluedollarcnt', 'taxvaluedollarcnt', 'assessmentyear', 'landtaxvaluedollarcnt',

    yardbuildingsqft26 = tf.contrib.layers.real_valued_column("yardbuildingsqft26")
    yearbuilt = tf.contrib.layers.real_valued_column("yearbuilt")
    numberofstories = tf.contrib.layers.real_valued_column("numberofstories")
    structuretaxvaluedollarcnt = tf.contrib.layers.real_valued_column("structuretaxvaluedollarcnt")
    taxvaluedollarcnt = tf.contrib.layers.real_valued_column("taxvaluedollarcnt")
    assessmentyear = tf.contrib.layers.real_valued_column("assessmentyear")
    landtaxvaluedollarcnt = tf.contrib.layers.real_valued_column("landtaxvaluedollarcnt")

    # 'taxamount', 'taxdelinquencyyear', 'censustractandblock']
    taxamount = tf.contrib.layers.real_valued_column("taxamount")
    taxdelinquencyyear = tf.contrib.layers.real_valued_column("taxdelinquencyyear")
    censustractandblock = tf.contrib.layers.real_valued_column("censustractandblock")

    # spsrse
    # ['hashottuborspa', 'fireplaceflag', 'taxdelinquencyflag']]
    hashottuborspa = tf.contrib.layers.sparse_column_with_keys(
        "hashottuborspa", keys=["False", "true"])
    fireplaceflag = tf.contrib.layers.sparse_column_with_keys(
        "fireplaceflag",  keys=["False", "true"])
    taxdelinquencyflag = tf.contrib.layers.sparse_column_with_keys(
        "taxdelinquencyflag", keys=["False", "N"])
    heatingorsystemtypeid = tf.contrib.layers.sparse_column_with_hash_bucket(
      "heatingorsystemtypeid", hash_bucket_size=1000)
    propertylandusetypeid = tf.contrib.layers.sparse_column_with_hash_bucket(
      "propertylandusetypeid", hash_bucket_size=1000)
    storytypeid = tf.contrib.layers.sparse_column_with_hash_bucket(
      "storytypeid", hash_bucket_size=1000)
    airconditioningtypeid = tf.contrib.layers.sparse_column_with_hash_bucket(
      "airconditioningtypeid", hash_bucket_size=1000)
    architecturalstyletypeid = tf.contrib.layers.sparse_column_with_hash_bucket(
      "architecturalstyletypeid", hash_bucket_size=1000)
    typeconstructiontypeid = tf.contrib.layers.sparse_column_with_hash_bucket(
      "typeconstructiontypeid", hash_bucket_size=1000)


    # Wide columns and deep columns.
    # continues columns feeding
    wide_columns = [#airconditioningtypeid,
                    #architecturalstyletypeid,
                    basementsqft, bathroomcnt, bedroomcnt,
                    buildingclasstypeid, buildingqualitytypeid, calculatedbathnbr, decktypeid, finishedfloor1squarefeet,
                    calculatedfinishedsquarefeet, finishedsquarefeet12, finishedsquarefeet13, finishedsquarefeet15,
                    finishedsquarefeet50, finishedsquarefeet6, fips, fireplacecnt, fullbathcnt, garagecarcnt,
                    garagetotalsqft,
                    #heatingorsystemtypeid,
                    latitude, longitude, lotsizesquarefeet, poolcnt,
                    poolsizesum, pooltypeid10, pooltypeid2, pooltypeid7,
                    #propertylandusetypeid,
                    rawcensustractandblock,
                    regionidcity, regionidcounty, regionidneighborhood, regionidzip, roomcnt,
                    #storytypeid,
                    threequarterbathnbr,
                    #typeconstructiontypeid,
                    unitcnt, yardbuildingsqft17, yardbuildingsqft26,
                    yearbuilt, numberofstories, structuretaxvaluedollarcnt, taxvaluedollarcnt, assessmentyear,
                    landtaxvaluedollarcnt, taxamount, taxdelinquencyyear, censustractandblock]
    # categorical columns + continuous feeding
    deep_columns = [
        tf.contrib.layers.embedding_column(hashottuborspa, dimension=8),
        tf.contrib.layers.embedding_column(fireplaceflag, dimension=8),
        tf.contrib.layers.embedding_column(taxdelinquencyflag, dimension=8),
        tf.contrib.layers.embedding_column(heatingorsystemtypeid, dimension=12),

        tf.contrib.layers.embedding_column(propertylandusetypeid, dimension=12),
        tf.contrib.layers.embedding_column(storytypeid, dimension=12),
        tf.contrib.layers.embedding_column(airconditioningtypeid, dimension=12),
        tf.contrib.layers.embedding_column(architecturalstyletypeid, dimension=12),
        tf.contrib.layers.embedding_column(typeconstructiontypeid, dimension=12),
        #airconditioningtypeid,
        #architecturalstyletypeid,
        basementsqft, bathroomcnt, bedroomcnt, buildingclasstypeid,
        buildingqualitytypeid, calculatedbathnbr, decktypeid, finishedfloor1squarefeet, calculatedfinishedsquarefeet,
        finishedsquarefeet12, finishedsquarefeet13, finishedsquarefeet15, finishedsquarefeet50, finishedsquarefeet6,
        fips, fireplacecnt, fullbathcnt, garagecarcnt, garagetotalsqft,
        #heatingorsystemtypeid,
        latitude, longitude,
        lotsizesquarefeet, poolcnt, poolsizesum, pooltypeid10, pooltypeid2, pooltypeid7,
        #propertylandusetypeid,
        rawcensustractandblock, regionidcity, regionidcounty, regionidneighborhood, regionidzip, roomcnt,
        #storytypeid,
        threequarterbathnbr,
        #typeconstructiontypeid,
        unitcnt, yardbuildingsqft17, yardbuildingsqft26, yearbuilt,
        numberofstories, structuretaxvaluedollarcnt, taxvaluedollarcnt, assessmentyear, landtaxvaluedollarcnt,
        taxamount, taxdelinquencyyear, censustractandblock
    ]

    if model_type == "wide":
        m = tf.contrib.learn.LinearClassifier(model_dir=model_dir,
                                              feature_columns=wide_columns)
    elif model_type == "deep":
        m = tf.contrib.learn.DNNClassifier(model_dir=model_dir,
                                           feature_columns=deep_columns,
                                           hidden_units=[1024, 512])
    elif model_type == "deenregress":
        m = tf.contrib.learn.DNNRegressor(model_dir=model_dir,
                                           feature_columns=deep_columns,
                                           hidden_units=[1024, 512])
    elif model_type == "wdRegress":
        m = tf.contrib.learn.DNNLinearCombinedRegressor(
            model_dir=model_dir,
            linear_feature_columns=wide_columns,
            linear_optimizer=tf.train.AdamOptimizer(learning_rate=0.00000001),
            dnn_feature_columns=deep_columns,
            dnn_hidden_units=[100, 50],
            dnn_optimizer=tf.train.AdamOptimizer(learning_rate=0.00000001),
            fix_global_step_increment_bug=True)
    else:
        m = tf.contrib.learn.DNNLinearCombinedClassifier(
            model_dir=model_dir,
            linear_feature_columns=wide_columns,
            dnn_feature_columns=deep_columns,
            dnn_hidden_units=[500, 200],
            fix_global_step_increment_bug=True)
    return m

#6.9556e+25
def input_fn(x_train,y_train ):
  """Input builder function."""
  # Creates a dictionary mapping from each continuous feature column name (k) to
  # the values of that column stored in a constant Tensor.
  continuous_cols = {k: tf.constant(x_train[k].values) for k in CONTINUOUS_COLUMNS}
  # Creates a dictionary mapping from each categorical feature column name (k)
  # to the values of that column stored in a tf.SparseTensor.
  categorical_cols2 = {
    k: tf.SparseTensor(
        indices=[[i, 0] for i in range(x_train[k].size)],
        values=x_train[k].astype(str).values,
        dense_shape=[x_train[k].size, 1])
        for k in CATEGORICAL_COLUMNS}


  # Merges the two dictionaries into one.
  feature_cols = dict(continuous_cols)
  feature_cols.update(categorical_cols2)
  # Converts the label column into a constant Tensor.
  label = tf.constant(y_train)
  # Returns the feature columns and the label.
  return feature_cols, label


def train_and_eval():
    """Train and evaluate the model."""
    # train_file_name, test_file_name = maybe_download(train_data, test_data)
    train = pd.read_csv('../train_2016_v2.csv')
    prop = pd.read_csv('../properties_2016.csv')
    sample = pd.read_csv('../sample_submission.csv')

    print('Creating training set ...')

    for c, dtype in zip(prop.columns, prop.dtypes):
        if dtype == np.float64:
            prop[c] = prop[c].fillna(0).astype(np.float32)

    df_train = train.merge(prop, how='left', on='parcelid')

    cat_cols = ["hashottuborspa", "propertycountylandusecode", "propertyzoningdesc", "fireplaceflag",
                "taxdelinquencyflag"]
    x_train = df_train.drop(
        ['parcelid', 'logerror', 'transactiondate', 'propertyzoningdesc', 'propertycountylandusecode']+cat_cols, axis=1)
    y_train = df_train['logerror'].values
    print(x_train.shape, y_train.shape)

    #train_y = train_df['logerror'].values
    # cat_cols = ["hashottuborspa", "propertycountylandusecode", "propertyzoningdesc", "fireplaceflag", "taxdelinquencyflag"]
    # train_df = x_train.drop(['parcelid', 'logerror', 'transactiondate', 'transaction_month']+cat_cols, axis=1)
    feat_names = x_train.columns.values

    from sklearn import ensemble
    import matplotlib.pyplot as plt
    plt.interactive(False)
    model = ensemble.ExtraTreesRegressor(n_estimators=25, max_depth=30, max_features=0.3, n_jobs=-1, random_state=0)
    model.fit(x_train, y_train)

    ## plot the importances ##
    importances = model.feature_importances_
    std = np.std([tree.feature_importances_ for tree in model.estimators_], axis=0)
    indices = np.argsort(importances)[::-1][:20]

    plt.figure(figsize=(12,12))
    plt.title("Feature importances")
    plt.bar(range(len(indices)), importances[indices], color="r", yerr=std[indices], align="center")
    plt.xticks(range(len(indices)), feat_names[indices], rotation='vertical')
    plt.xlim([-1, len(indices)])
    plt.show()


import argparse
import sys
import tempfile


train_and_eval()


