from debug import utils
import json, cgi, sys
import plot_litchi_grid

class Waypoints():
    def __init__(self):
        utils.Traceback()
        data = cgi.FieldStorage()
        utils.Log(data)
        name = data.getvalue('name')
        if name == "main":
            self.create_waypoints(data)
        else:
            self.send_json("andy")

    def create_waypoints(self, data):
        waypoint_data = plot_litchi_grid.calulate_points(float(data.getvalue('lat')), 
                                                         float(data.getvalue('lon')),
                                                         float(data.getvalue('dist_between_waypoints')),
                                                         float(data.getvalue('drone_heading')),
                                                         float(data.getvalue('camera_heading')),
                                                         float(data.getvalue('gimbal_pitch')),
                                                         int(data.getvalue('num_rows')),
                                                         int(data.getvalue('num_cols')),
                                                         float(data.getvalue('drone_height')))
        self.send_json(waypoint_data)

    def send_json(self, text):
        response = {'success':'true','text':text}
        utils.Traceback(response)
        print('Content-type: application/json\n')
        print(json.dumps(response))
