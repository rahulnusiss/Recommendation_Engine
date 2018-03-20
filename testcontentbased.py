from ContentBased import content_engine
import json
# Test for csv
# content_engine.train('mentorica_article_test.csv')

json_data = json.loads('{"color" : "blue", "gender" : "1"}');
print ( json_data);
# Test for postgres
print(content_engine.trainFeature(json_data));

