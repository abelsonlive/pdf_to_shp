import json
import sys

def rescale_geojson(from_path, to_path, out_path):
  """
  given an input geojson file <from_path> rescale the
  file's coordinate system to the the bounds of a 
  reference geo_json file <to_path>, and write this
  file to <out_path>
  """
  # load data
  from_dict = json.load(open(from_path))
  to_dict = json.load(open(to_path))

  # calculate bounds
  from_bounds = calc_bounds(from_dict)
  to_bounds = calc_bounds(to_dict)
  
  print "< from-bounds:", from_bounds, " >"
  print "< to-bounds: ", to_bounds, " >"

  # generate scaling functions
  x = ScaleFX(
    from_bounds['xmin'], 
    from_bounds['xmax'], 
    to_bounds['xmin'], 
    to_bounds['xmax'])

  # generate scaling functions
  y = ScaleFX(
    from_bounds['ymin'], 
    from_bounds['ymax'], 
    to_bounds['ymin'], 
    to_bounds['ymax']
  )

  # rescale coordinates
  scaled_data = re_scale_geojson(from_dict, x.scale, y.scale)
  scaled_bounds = calc_bounds(scaled_data)
  print "< intially-scaled-bounds: ", scaled_bounds, " >"

  # for some reason my algorithm doesnt work and I need a slight correction?
  final_data = correct_geo_json(scaled_data, scaled_bounds, to_bounds)
  final_bounds = calc_bounds(final_data)
  print "< final bounds: ", final_bounds, " >"

  if out_path:
    with open(out_path, 'wb') as f:
      f.write(json.dumps(final_data, indent=4))
  else:
    return final_data

def correct_geo_json(d, scaled_bounds, to_bounds):
  """
  HACK: rescale the file once more for increased accuracy.
  """
  # slight adjustments
  f_x = scaled_bounds['xmax'] - to_bounds['xmax']
  f_y = scaled_bounds['ymax'] - to_bounds['ymax']
  x = ScaleFX(f=f_x)
  y = ScaleFX(f=f_y)
  
  return re_scale_geojson(d, x.scale, y.scale)

def re_scale_geojson(d, x_scale, y_scale):
  """
  given a geojson dictionary and two scaling functions, 
  return an identical dictionary with rescaled coordinates
  """
  new_data = {}

  # rescale data
  for i, feature in enumerate(d['features']):
    new_coords = []
    for coord in feature['geometry']['coordinates'][0]:
      # overwrite coordinates
      old_x = coord[0]
      old_y = coord[1]
      new_x = x_scale(old_x)
      new_y = y_scale(old_y)

      new_coords.append([new_x, new_y])

    d['features'][i]['geometry']['coordinates'] = [new_coords]

  return d

class ScaleFX(object):
  """
  Given the min and max of the coordinate system of two geojsons, 
  generate a fx to rescale these coordinates from one system to 
  the other
  """

  def __init__(self, from_min=None, from_max=None, to_min=None, to_max=None, f=None):
    self.from_min = from_min
    self.from_max = from_max
    self.to_min = to_min
    self.to_max = to_max
    self.f = f

  def scale(self, v):
    if self.f:
      return v - self.f
    else:
      return (((v - self.from_min) * (self.to_max - self.to_min)) / 
      (self.from_max - self.from_min)) + self.to_max


def calc_bounds(d):
  """
  given a geojson dictionary, return x and y bounds of the shape:

  {
    xmin: ,
    xmax: ,
    ymin: ,
    ymax ,
  }
  """
  features = d['features']

  #unnest data
  x_coords = []
  y_coords = []
  for feature in features:
    for coord in feature['geometry']['coordinates'][0]:
      x_coords.append(coord[0])
      y_coords.append(coord[1])

  return {
    'xmin': min(x_coords),
    'xmax': max(x_coords),
    'ymin': min(y_coords),
    'ymax': max(y_coords)
  }

if __name__ == '__main__':
  d = sys.argv[1].upper()
  print "< rescaling: %s >" % d
  rescale_geojson(
    'raw_geojson/%s.geojson' % d, 
    'divisions_geojson/%s.geojson' % d,
    'villages_geojson/%s.geojson' % d
  )