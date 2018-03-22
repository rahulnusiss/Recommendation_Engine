from ContentBased import content_engine
import json
# Test for csv
# content_engine.train('mentorica_article_test.csv')

json_data = json.loads('{"color" : "black", "gender" : "1", "age" : "20"}');
print ( json_data);
# Test for postgres
print(content_engine.trainFeature(json_data));

