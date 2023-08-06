## Tf-idf Transformation


###  Install

```
$ pip install tfidf_transformation_brk
```


### Usage

Open a Python console, import the module TfidfTransformer, create an instance of it and you can call its fit(), transform(), fit_transform() or get_feature_names() methods.

```
>> from tfidf_transformation_brk import TfidfTransformer
>>
>> tfidf = TfidfTransformer()
>> tfidf.fit(documents)
>>
>> fit_transform = tfidf.fit_transform(documents)
>> 
>>feature_names = tfidf.get_feature_names()
```


### License

This project is licensed under the MIT License


### Author

Berk Ozturk