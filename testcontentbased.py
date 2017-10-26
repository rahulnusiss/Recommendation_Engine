from ContentBased import content_engine
import json
# Test for csv
# content_engine.train('mentorica_article_test.csv')

json_data = json.loads('{"color" : "black", "gender" : "MEN", "description" : "jacket"}');
print ( json_data['color'] );
# Test for postgres
content_engine.trainFeature(json_data)

