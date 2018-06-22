import unittest
from rest_framework import status
from rest_framework.test import APIClient
from shortest_route_app.models import FileMap, Map
from shortest_route_app.serializers.FileMapSerializer import FileMapSerializer
from shortest_route_app.utils.Utils import is_number


class TestShortestRoute(unittest.TestCase):
    end_point = '/api/'
    json_valid = {
        "name": "valid_json",
        "map": [
            {"first_edge": "A",
              "second_edge": "B",
              "value": 10},
            {"first_edge": "B",
              "second_edge": "D",
              "value": 15},
            {"first_edge": "A",
              "second_edge": "C",
              "value": 20},
            {"first_edge": "C",
              "second_edge": "D",
              "value": 30},
            {"first_edge": "B",
              "second_edge": "E",
              "value": 50},
            {"first_edge": "D",
              "second_edge": "E",
              "value": 30}
        ]
    }

    json_invalid = {
        "name": "invalid_json",
        "map": [
            {"first_edge": "A",
             "second_edge": "B",
             "value": 10},
            {"first_edge": "B",
             "a": "D",
             "value": 15},
            {"first_edge": "A",
             "value": 20},
            {"first_edge": "C",
             "second_edge": "D",
             "value": 30},
            {"first_edge": "B",
             "second_edge": "E",
             "value": 50},
            {"first_edge": "D",
             "second_edge": "E",
             "value": 30}
        ]
    }

    json_name = {
        "name": "valid_json",
        "map": [
            {"first_edge": "A",
             "second_edge": "B",
             "value": 10}
        ]
    }

    json_space = {
        "name": "space json",
        "map": [
            {"first_edge": "A",
              "second_edge": "B",
              "value": 10},
            {"first_edge": "B",
              "second_edge": "D",
              "value": 15},
            {"first_edge": "A",
              "second_edge": "C",
              "value": 20},
            {"first_edge": "C",
              "second_edge": "D",
              "value": 30},
            {"first_edge": "B",
              "second_edge": "E",
              "value": 50},
            {"first_edge": "D",
              "second_edge": "E",
              "value": 30}
        ]
    }

    json_repeat = {
        "name": "repeat_json",
        "map": [
            {"first_edge": "A",
              "second_edge": "B",
              "value": 10},
            {"first_edge": "B",
              "second_edge": "D",
              "value": 15},
            {"first_edge": "A",
              "second_edge": "C",
              "value": 20},
            {"first_edge": "C",
              "second_edge": "D",
              "value": 30},
            {"first_edge": "B",
              "second_edge": "A",
              "value": 5},
            {"first_edge": "D",
              "second_edge": "E",
              "value": 30}
        ]
    }

    json_new = {
        "name": "new_json",
        "map": [
            {"first_edge": "A",
             "second_edge": "B",
             "value": 10},
            {"first_edge": "B",
             "second_edge": "D",
             "value": 15},
            {"first_edge": "A",
             "second_edge": "C",
             "value": 20},
            {"first_edge": "C",
             "second_edge": "D",
             "value": 30},
            {"first_edge": "B",
             "second_edge": "E",
             "value": 50},
            {"first_edge": "D",
             "second_edge": "E",
             "value": 30}
        ]
    }
    """
    before each test the setUP is used to create a json and at the end of the test uses the tearDown to destroy
    """
    def setUp(self):
        self.client = APIClient()
        response = self.client.post(self.end_point + "map/", self.json_valid, format='json')
        self.pk = response.data['id']

    def tearDown(self):
        self.client.delete(self.end_point + "map/" + str(self.pk) + "/")

    def test_is_number(self):
        self.assertTrue(is_number(7))

    def test_is_not_number(self):
        self.assertFalse(is_number('a'))

    def test_save_exist_map(self):
        response = self.client.post(self.end_point + "map/", self.json_valid, format='json')
        self.assertEqual(response.status_code, 400)

    def test_save_invalid_map(self):
        response = self.client.post(self.end_point + "map/", self.json_invalid, format='json')
        self.assertEqual(response.status_code, 400)

    def test_save_same_name_map(self):
        response = self.client.post(self.end_point + "map/", self.json_valid, format='json')
        self.assertEqual(response.status_code, 400)

    def test_save_map(self):
        response = self.client.post(self.end_point + "map/", self.json_new, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_maps(self):
        response = self.client.get(self.end_point + "map/")
        maps_list = FileMap.objects.all()
        result = []
        for map in maps_list:
            result.append("id:" + str(map.id) + "; nome:" + map.name)
        self.assertEqual(response.data, {'maps': result})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_map(self):
        response = self.client.get(self.end_point + "map/"+str(self.pk)+"/")
        file_map = FileMap.objects.get(pk=self.pk)
        serializer = FileMapSerializer(file_map)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_map(self):
        response = self.client.put(self.end_point + "map/" + str(self.pk) + "/", self.json_new, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_map(self):
        response = self.client.delete(self.end_point + "map/" + str(self.pk) + "/")
        self.assertEqual(response.status_code, 204)

    def test_get_points(self):
        response = self.client.get(self.end_point + "points/")
        points_list = Map.objects.all()
        result = []
        for point in points_list:
            result.append(
                "map_id:" + point.file_id.name + "; first_edge:" + point.first_edge + "; second_edge:" + point.second_edge + "; value:" + str(
                    point.value))

        self.assertEqual(response.data, {'maps': result})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shortest_route(self):
        url = 'shortest_route/valid_json/A/D/10/2.5/'
        correct = "best_route:['A', 'B', 'D']; cost:6.25;"
        response = self.client.get(self.end_point + url)
        self.assertEqual(response.data, correct)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shortest_route_downcase_url(self):
        url = 'shortest_route/valid_json/a/d/10/2.5/'
        correct = "best_route:['A', 'B', 'D']; cost:6.25;"
        response = self.client.get(self.end_point + url)
        self.assertEqual(response.data, correct)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shortest_route_inexistent_point(self):
        url = 'shortest_route/valid_json/Z/D/10/2.5/'
        error = "Point of origin not found on the map."
        response = self.client.get(self.end_point + url)
        self.assertEqual(response.data, error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_shortest_route_wrong_url(self):
        url = 'shortest_route/valid_json/2!!@/D/10/2.5/'
        response = self.client.get(self.end_point + url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_shortest_route_wrong_values(self):
        url = 'shortest_route/valid_json/A/D/A/2.5/'
        response = self.client.get(self.end_point + url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_shortest_route_inexistent_map(self):
        url = 'shortest_route/not_map/A/D/10/2/'
        error = "No map with this name was found."
        response = self.client.get(self.end_point + url)
        self.assertEqual(response.data, error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_shortest_route_very_long_map(self):
        url = 'shortest_route/teste11/A/D/10/2/'

    def test_shortest_route_space_name_map(self):
        save = self.client.post(self.end_point + "map/", self.json_space, format='json')
        url = 'shortest_route/space json/A/D/10/2.5/'
        correct = "best_route:['A', 'B', 'D']; cost:6.25;"
        response = self.client.get(self.end_point + url)
        self.assertEqual(response.data, correct)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shortest_route_repeat_points(self):
        save = self.client.post(self.end_point + "map/", self.json_repeat, format='json')
        url = 'shortest_route/repeat_json/A/D/10/2.5/'
        correct = "best_route:['A', 'B', 'D']; cost:5.0;"
        response = self.client.get(self.end_point + url)
        self.assertEqual(response.data, correct)
        self.assertEqual(response.status_code, status.HTTP_200_OK)