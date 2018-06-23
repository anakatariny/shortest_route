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
        url = 'shortest_route/map_large/A/L/10/2.5/'
        correct = "best_route:['A', 'U', 'T', 'L']; cost:247.0;"
        response = self.client.get(self.end_point + url)
        self.assertEqual(response.data, correct)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shortest_route_space_name_map(self):
        self.client.post(self.end_point + "map/", self.json_space, format='json')
        url = 'shortest_route/space json/A/D/10/2.5/'
        correct = "best_route:['A', 'B', 'D']; cost:6.25;"
        response = self.client.get(self.end_point + url)
        self.assertEqual(response.data, correct)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shortest_route_repeat_points(self):
        self.client.post(self.end_point + "map/", self.json_repeat, format='json')
        url = 'shortest_route/repeat_json/A/D/10/2.5/'
        correct = "best_route:['A', 'B', 'D']; cost:5.0;"
        response = self.client.get(self.end_point + url)
        self.assertEqual(response.data, correct)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    json_map_large = {
        "name": "map_large",
        "map": [
            {
                "first_edge": "G",
                "second_edge": "C",
                "value": 785
            },
            {
                "first_edge": "M",
                "second_edge": "H",
                "value": 924
            },
            {
                "first_edge": "L",
                "second_edge": "E",
                "value": 363
            },
            {
                "first_edge": "T",
                "second_edge": "Q",
                "value": 877
            },
            {
                "first_edge": "Z",
                "second_edge": "Z",
                "value": 618
            },
            {
                "first_edge": "K",
                "second_edge": "O",
                "value": 520
            },
            {
                "first_edge": "D",
                "second_edge": "H",
                "value": 234
            },
            {
                "first_edge": "H",
                "second_edge": "G",
                "value": 442
            },
            {
                "first_edge": "L",
                "second_edge": "F",
                "value": 825
            },
            {
                "first_edge": "K",
                "second_edge": "R",
                "value": 693
            },
            {
                "first_edge": "V",
                "second_edge": "K",
                "value": 102
            },
            {
                "first_edge": "V",
                "second_edge": "R",
                "value": 720
            },
            {
                "first_edge": "O",
                "second_edge": "C",
                "value": 430
            },
            {
                "first_edge": "A",
                "second_edge": "F",
                "value": 376
            },
            {
                "first_edge": "F",
                "second_edge": "W",
                "value": 597
            },
            {
                "first_edge": "Q",
                "second_edge": "N",
                "value": 705
            },
            {
                "first_edge": "D",
                "second_edge": "N",
                "value": 636
            },
            {
                "first_edge": "T",
                "second_edge": "Q",
                "value": 745
            },
            {
                "first_edge": "U",
                "second_edge": "A",
                "value": 555
            },
            {
                "first_edge": "Z",
                "second_edge": "V",
                "value": 892
            },
            {
                "first_edge": "C",
                "second_edge": "A",
                "value": 871
            },
            {
                "first_edge": "U",
                "second_edge": "E",
                "value": 304
            },
            {
                "first_edge": "M",
                "second_edge": "G",
                "value": 954
            },
            {
                "first_edge": "N",
                "second_edge": "B",
                "value": 103
            },
            {
                "first_edge": "U",
                "second_edge": "S",
                "value": 663
            },
            {
                "first_edge": "R",
                "second_edge": "M",
                "value": 597
            },
            {
                "first_edge": "X",
                "second_edge": "Z",
                "value": 672
            },
            {
                "first_edge": "H",
                "second_edge": "B",
                "value": 486
            },
            {
                "first_edge": "E",
                "second_edge": "A",
                "value": 872
            },
            {
                "first_edge": "Z",
                "second_edge": "H",
                "value": 227
            },
            {
                "first_edge": "C",
                "second_edge": "T",
                "value": 392
            },
            {
                "first_edge": "M",
                "second_edge": "A",
                "value": 391
            },
            {
                "first_edge": "T",
                "second_edge": "J",
                "value": 240
            },
            {
                "first_edge": "D",
                "second_edge": "J",
                "value": 396
            },
            {
                "first_edge": "X",
                "second_edge": "K",
                "value": 311
            },
            {
                "first_edge": "Q",
                "second_edge": "Q",
                "value": 450
            },
            {
                "first_edge": "U",
                "second_edge": "T",
                "value": 188
            },
            {
                "first_edge": "U",
                "second_edge": "Z",
                "value": 116
            },
            {
                "first_edge": "D",
                "second_edge": "J",
                "value": 534
            },
            {
                "first_edge": "U",
                "second_edge": "K",
                "value": 258
            },
            {
                "first_edge": "G",
                "second_edge": "F",
                "value": 615
            },
            {
                "first_edge": "A",
                "second_edge": "C",
                "value": 889
            },
            {
                "first_edge": "W",
                "second_edge": "U",
                "value": 944
            },
            {
                "first_edge": "U",
                "second_edge": "Q",
                "value": 733
            },
            {
                "first_edge": "A",
                "second_edge": "Y",
                "value": 567
            },
            {
                "first_edge": "M",
                "second_edge": "W",
                "value": 530
            },
            {
                "first_edge": "Y",
                "second_edge": "U",
                "value": 876
            },
            {
                "first_edge": "Y",
                "second_edge": "G",
                "value": 565
            },
            {
                "first_edge": "M",
                "second_edge": "V",
                "value": 710
            },
            {
                "first_edge": "V",
                "second_edge": "E",
                "value": 284
            },
            {
                "first_edge": "B",
                "second_edge": "E",
                "value": 206
            },
            {
                "first_edge": "S",
                "second_edge": "M",
                "value": 514
            },
            {
                "first_edge": "H",
                "second_edge": "G",
                "value": 769
            },
            {
                "first_edge": "A",
                "second_edge": "Z",
                "value": 830
            },
            {
                "first_edge": "B",
                "second_edge": "Q",
                "value": 521
            },
            {
                "first_edge": "B",
                "second_edge": "I",
                "value": 832
            },
            {
                "first_edge": "J",
                "second_edge": "A",
                "value": 773
            },
            {
                "first_edge": "M",
                "second_edge": "T",
                "value": 470
            },
            {
                "first_edge": "A",
                "second_edge": "P",
                "value": 547
            },
            {
                "first_edge": "O",
                "second_edge": "Q",
                "value": 665
            },
            {
                "first_edge": "U",
                "second_edge": "I",
                "value": 686
            },
            {
                "first_edge": "J",
                "second_edge": "L",
                "value": 585
            },
            {
                "first_edge": "U",
                "second_edge": "C",
                "value": 753
            },
            {
                "first_edge": "W",
                "second_edge": "V",
                "value": 129
            },
            {
                "first_edge": "C",
                "second_edge": "C",
                "value": 755
            },
            {
                "first_edge": "N",
                "second_edge": "Z",
                "value": 325
            },
            {
                "first_edge": "C",
                "second_edge": "O",
                "value": 358
            },
            {
                "first_edge": "G",
                "second_edge": "U",
                "value": 554
            },
            {
                "first_edge": "N",
                "second_edge": "Y",
                "value": 296
            },
            {
                "first_edge": "T",
                "second_edge": "B",
                "value": 984
            },
            {
                "first_edge": "V",
                "second_edge": "X",
                "value": 850
            },
            {
                "first_edge": "J",
                "second_edge": "I",
                "value": 461
            },
            {
                "first_edge": "B",
                "second_edge": "Y",
                "value": 720
            },
            {
                "first_edge": "C",
                "second_edge": "Q",
                "value": 218
            },
            {
                "first_edge": "Y",
                "second_edge": "Y",
                "value": 700
            },
            {
                "first_edge": "W",
                "second_edge": "Q",
                "value": 298
            },
            {
                "first_edge": "W",
                "second_edge": "W",
                "value": 581
            },
            {
                "first_edge": "H",
                "second_edge": "Z",
                "value": 847
            },
            {
                "first_edge": "L",
                "second_edge": "L",
                "value": 872
            },
            {
                "first_edge": "O",
                "second_edge": "Q",
                "value": 999
            },
            {
                "first_edge": "P",
                "second_edge": "H",
                "value": 397
            },
            {
                "first_edge": "V",
                "second_edge": "H",
                "value": 352
            },
            {
                "first_edge": "U",
                "second_edge": "J",
                "value": 892
            },
            {
                "first_edge": "I",
                "second_edge": "M",
                "value": 711
            },
            {
                "first_edge": "K",
                "second_edge": "S",
                "value": 643
            },
            {
                "first_edge": "I",
                "second_edge": "K",
                "value": 886
            },
            {
                "first_edge": "R",
                "second_edge": "O",
                "value": 975
            },
            {
                "first_edge": "F",
                "second_edge": "K",
                "value": 978
            },
            {
                "first_edge": "E",
                "second_edge": "N",
                "value": 391
            },
            {
                "first_edge": "B",
                "second_edge": "K",
                "value": 875
            },
            {
                "first_edge": "C",
                "second_edge": "X",
                "value": 549
            },
            {
                "first_edge": "M",
                "second_edge": "G",
                "value": 487
            },
            {
                "first_edge": "E",
                "second_edge": "A",
                "value": 884
            },
            {
                "first_edge": "T",
                "second_edge": "I",
                "value": 108
            },
            {
                "first_edge": "C",
                "second_edge": "P",
                "value": 596
            },
            {
                "first_edge": "Z",
                "second_edge": "F",
                "value": 309
            },
            {
                "first_edge": "E",
                "second_edge": "A",
                "value": 451
            },
            {
                "first_edge": "J",
                "second_edge": "D",
                "value": 111
            },
            {
                "first_edge": "V",
                "second_edge": "N",
                "value": 838
            },
            {
                "first_edge": "O",
                "second_edge": "D",
                "value": 763
            },
            {
                "first_edge": "J",
                "second_edge": "J",
                "value": 715
            },
            {
                "first_edge": "Q",
                "second_edge": "C",
                "value": 535
            },
            {
                "first_edge": "P",
                "second_edge": "I",
                "value": 297
            },
            {
                "first_edge": "W",
                "second_edge": "V",
                "value": 891
            },
            {
                "first_edge": "D",
                "second_edge": "B",
                "value": 719
            },
            {
                "first_edge": "N",
                "second_edge": "B",
                "value": 731
            },
            {
                "first_edge": "Q",
                "second_edge": "A",
                "value": 523
            },
            {
                "first_edge": "X",
                "second_edge": "X",
                "value": 494
            },
            {
                "first_edge": "A",
                "second_edge": "A",
                "value": 581
            },
            {
                "first_edge": "G",
                "second_edge": "N",
                "value": 238
            },
            {
                "first_edge": "S",
                "second_edge": "S",
                "value": 174
            },
            {
                "first_edge": "Y",
                "second_edge": "Y",
                "value": 521
            },
            {
                "first_edge": "V",
                "second_edge": "X",
                "value": 332
            },
            {
                "first_edge": "T",
                "second_edge": "S",
                "value": 596
            },
            {
                "first_edge": "G",
                "second_edge": "O",
                "value": 693
            },
            {
                "first_edge": "R",
                "second_edge": "O",
                "value": 876
            },
            {
                "first_edge": "C",
                "second_edge": "N",
                "value": 978
            },
            {
                "first_edge": "W",
                "second_edge": "P",
                "value": 535
            },
            {
                "first_edge": "N",
                "second_edge": "J",
                "value": 868
            },
            {
                "first_edge": "C",
                "second_edge": "K",
                "value": 829
            },
            {
                "first_edge": "P",
                "second_edge": "E",
                "value": 341
            },
            {
                "first_edge": "U",
                "second_edge": "W",
                "value": 903
            },
            {
                "first_edge": "L",
                "second_edge": "D",
                "value": 638
            },
            {
                "first_edge": "C",
                "second_edge": "W",
                "value": 291
            },
            {
                "first_edge": "X",
                "second_edge": "R",
                "value": 499
            },
            {
                "first_edge": "B",
                "second_edge": "Z",
                "value": 667
            },
            {
                "first_edge": "L",
                "second_edge": "T",
                "value": 245
            },
            {
                "first_edge": "G",
                "second_edge": "I",
                "value": 465
            },
            {
                "first_edge": "A",
                "second_edge": "A",
                "value": 271
            },
            {
                "first_edge": "Q",
                "second_edge": "P",
                "value": 268
            },
            {
                "first_edge": "U",
                "second_edge": "Z",
                "value": 281
            },
            {
                "first_edge": "U",
                "second_edge": "J",
                "value": 350
            },
            {
                "first_edge": "Y",
                "second_edge": "J",
                "value": 763
            },
            {
                "first_edge": "I",
                "second_edge": "M",
                "value": 545
            },
            {
                "first_edge": "C",
                "second_edge": "R",
                "value": 684
            },
            {
                "first_edge": "O",
                "second_edge": "U",
                "value": 264
            },
            {
                "first_edge": "C",
                "second_edge": "J",
                "value": 402
            },
            {
                "first_edge": "M",
                "second_edge": "K",
                "value": 641
            },
            {
                "first_edge": "Q",
                "second_edge": "P",
                "value": 496
            },
            {
                "first_edge": "V",
                "second_edge": "O",
                "value": 646
            },
            {
                "first_edge": "W",
                "second_edge": "A",
                "value": 446
            },
            {
                "first_edge": "N",
                "second_edge": "S",
                "value": 313
            },
            {
                "first_edge": "H",
                "second_edge": "Q",
                "value": 896
            },
            {
                "first_edge": "K",
                "second_edge": "D",
                "value": 936
            },
            {
                "first_edge": "E",
                "second_edge": "K",
                "value": 422
            },
            {
                "first_edge": "H",
                "second_edge": "B",
                "value": 216
            },
            {
                "first_edge": "K",
                "second_edge": "N",
                "value": 321
            },
            {
                "first_edge": "I",
                "second_edge": "U",
                "value": 579
            },
            {
                "first_edge": "S",
                "second_edge": "W",
                "value": 783
            },
            {
                "first_edge": "T",
                "second_edge": "G",
                "value": 755
            },
            {
                "first_edge": "S",
                "second_edge": "W",
                "value": 384
            },
            {
                "first_edge": "A",
                "second_edge": "F",
                "value": 821
            },
            {
                "first_edge": "E",
                "second_edge": "Y",
                "value": 696
            },
            {
                "first_edge": "V",
                "second_edge": "Q",
                "value": 749
            },
            {
                "first_edge": "N",
                "second_edge": "V",
                "value": 637
            },
            {
                "first_edge": "M",
                "second_edge": "Z",
                "value": 334
            },
            {
                "first_edge": "S",
                "second_edge": "H",
                "value": 293
            },
            {
                "first_edge": "C",
                "second_edge": "U",
                "value": 738
            },
            {
                "first_edge": "M",
                "second_edge": "E",
                "value": 969
            },
            {
                "first_edge": "V",
                "second_edge": "C",
                "value": 976
            },
            {
                "first_edge": "B",
                "second_edge": "F",
                "value": 218
            },
            {
                "first_edge": "Z",
                "second_edge": "Q",
                "value": 809
            },
            {
                "first_edge": "W",
                "second_edge": "R",
                "value": 992
            },
            {
                "first_edge": "T",
                "second_edge": "Z",
                "value": 752
            },
            {
                "first_edge": "D",
                "second_edge": "H",
                "value": 865
            },
            {
                "first_edge": "R",
                "second_edge": "N",
                "value": 303
            },
            {
                "first_edge": "V",
                "second_edge": "H",
                "value": 461
            },
            {
                "first_edge": "I",
                "second_edge": "C",
                "value": 944
            },
            {
                "first_edge": "K",
                "second_edge": "E",
                "value": 592
            },
            {
                "first_edge": "A",
                "second_edge": "X",
                "value": 261
            },
            {
                "first_edge": "B",
                "second_edge": "V",
                "value": 933
            },
            {
                "first_edge": "O",
                "second_edge": "G",
                "value": 406
            },
            {
                "first_edge": "J",
                "second_edge": "O",
                "value": 818
            },
            {
                "first_edge": "B",
                "second_edge": "G",
                "value": 968
            },
            {
                "first_edge": "I",
                "second_edge": "R",
                "value": 942
            },
            {
                "first_edge": "C",
                "second_edge": "A",
                "value": 577
            },
            {
                "first_edge": "W",
                "second_edge": "M",
                "value": 241
            },
            {
                "first_edge": "M",
                "second_edge": "Y",
                "value": 949
            },
            {
                "first_edge": "K",
                "second_edge": "B",
                "value": 347
            },
            {
                "first_edge": "F",
                "second_edge": "K",
                "value": 123
            },
            {
                "first_edge": "Z",
                "second_edge": "W",
                "value": 324
            },
            {
                "first_edge": "Z",
                "second_edge": "X",
                "value": 426
            },
            {
                "first_edge": "B",
                "second_edge": "A",
                "value": 674
            },
            {
                "first_edge": "Z",
                "second_edge": "K",
                "value": 616
            },
            {
                "first_edge": "B",
                "second_edge": "K",
                "value": 298
            },
            {
                "first_edge": "U",
                "second_edge": "Z",
                "value": 287
            },
            {
                "first_edge": "C",
                "second_edge": "O",
                "value": 135
            },
            {
                "first_edge": "G",
                "second_edge": "J",
                "value": 621
            },
            {
                "first_edge": "N",
                "second_edge": "F",
                "value": 487
            },
            {
                "first_edge": "T",
                "second_edge": "I",
                "value": 492
            },
            {
                "first_edge": "C",
                "second_edge": "P",
                "value": 824
            },
            {
                "first_edge": "J",
                "second_edge": "N",
                "value": 696
            },
            {
                "first_edge": "R",
                "second_edge": "Z",
                "value": 399
            },
            {
                "first_edge": "C",
                "second_edge": "P",
                "value": 473
            },
            {
                "first_edge": "M",
                "second_edge": "D",
                "value": 337
            },
            {
                "first_edge": "Y",
                "second_edge": "Q",
                "value": 789
            },
            {
                "first_edge": "O",
                "second_edge": "O",
                "value": 152
            },
            {
                "first_edge": "U",
                "second_edge": "L",
                "value": 682
            },
            {
                "first_edge": "T",
                "second_edge": "B",
                "value": 286
            },
            {
                "first_edge": "O",
                "second_edge": "H",
                "value": 643
            }
        ]
    }