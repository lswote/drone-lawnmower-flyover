#!/usr/bin/env python
import os, sys
from math import sin, cos, radians, pi
from pyproj import Proj, transform
from debug import utils

# per http://spatialreference.org/ref/epsg/
# EPSG Projection List
fleast_ft = Proj(init='esri:102658') # NAD_1983_StatePlane_Florida_East_FIPS_0901_Feet
fleast_m = Proj(init='esri:102258')  # NAD_1983_HARN_StatePlane_Florida_East_FIPS_0901
wgs84 = Proj(proj='latlong',datum='WGS84')
M2FT = 3.2808399
FT2M = (1.0/M2FT)

def point_pos(x0, y0, d, theta):
    theta_rad = pi/2 - radians(theta)
    return x0 + d*cos(theta_rad), y0 + d*sin(theta_rad)

def getPlaneCoordinates(lat, lon):
    x, y, z = transform(wgs84,fleast_m,lon,lat,0.0)
    return x*M2FT,y*M2FT

def getGeoCoordinates(x, y):
    lat, lon, depth = transform(fleast_m,wgs84,x*FT2M,y*FT2M,0.0)
    return lon, lat

#  lat, lon of southwest corner of property
def calulate_points(lat, lon, dist_between_waypoints, drone_heading, camera_heading, gimbal_pitch, num_rows, num_cols, drone_height):
    utils.Log(lat, lon, dist_between_waypoints, drone_heading, camera_heading, gimbal_pitch, num_rows, num_cols, drone_height)
    half_dist = dist_between_waypoints/2
    x,y = getPlaneCoordinates(lat, lon)
    waypoint_data = "latitude,longitude,altitude(ft),heading(deg),curvesize(ft),rotationdir,gimbalmode,gimbalpitchangle,actiontype1,actionparam1,actiontype2,actionparam2,actiontype3,actionparam3,actiontype4,actionparam4,actiontype5,actionparam5,actiontype6,actionparam6,actiontype7,actionparam7,actiontype8,actionparam8,actiontype9,actionparam9,actiontype10,actionparam10,actiontype11,actionparam11,actiontype12,actionparam12,actiontype13,actionparam13,actiontype14,actionparam14,actiontype15,actionparam15\n"
    for i in range(0,num_cols):
        col_offset = half_dist*(2*i+1)
        x1, y1 = point_pos(x, y, col_offset, (drone_heading+90)%360)
        for j in range(0,num_rows):
            if i % 2:
                row_offset = half_dist*((num_rows-j)*2-2)
            else:
                row_offset = half_dist*(2*j)
            x2, y2 = point_pos(x1, y1, row_offset, drone_heading)
            lat2, lon2 = getGeoCoordinates(x2, y2)
            # the computed values
            waypoint_data += ",".join([str(lat2),str(lon2),str(drone_height),str(camera_heading)])
            # the hardcoded values - set gimbel pitch to interpolate and gimbel angle to straight down, add action to take photo
            waypoint_data += ",".join([",0,0,2",str(gimbal_pitch),"1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0\n"])
    return(waypoint_data)

if __name__ == '__main__':
    # lat, lon, dist_between_waypoints, drone_heading, camera_heading, gimbal_pitch, num_rows, num_cols, drone_height
    waypoint_data = calulate_points(26.127615, -80.423109, 12, 16, 10, -90, 6, 3, 40)
    #waypoint_data = calulate_points(26.127615, -80.423109, 14, 16, 280, -60, 6, 4, 35)
    f = open('waypoints.csv', 'w')
    f.write(waypoint_data)
