from typing import List

class LabelledDatapoint:
  def __init__(self, feature_values: List[bool], label: str):
    self.feature_values = feature_values
    self.label = label

  def get_feature_values(self) -> List[bool]:
    return self.feature_values

  def get_feature_value(self, i: int) -> bool:
    return self.feature_values[i]

  def get_label(self) -> str:
    return self.label

# n datapoints
# k features
# for each of the n datapoints:
#   - k boolean values, the feature values
#   - 1 label
class LabelledDataSet:
  def __init__(self, feature_names: List[str], datapoints: List[LabelledDatapoint]) -> None:
    self.feature_names = feature_names
    self.datapoints = datapoints

  def filter(self, filter_fn):
    return LabelledDataSet(self.feature_names, list(filter(filter_fn, self.datapoints)))

  # count predicate over label
  def count_label_predicate(self, label_predicate):
    labels = map(lambda dp: dp.get_label(), self.datapoints)
    return sum(1 for _ in filter(label_predicate, labels))

  def get_datapoints(self) -> List[LabelledDatapoint]:
    return self.datapoints

  def get_feature_names(self) -> List[str]:
    return self.feature_names

  def get_feature_values(self, i: int) -> List[bool]:
    return self.datapoints[i].get_feature_values()

  def get_feature_value(self, i: int, j: int) -> bool:
    return self.get_feature_values(i)[j]

  def get_label(self, i: int) -> str:
    return self.datapoints[i].get_label()

  def size(self):
    return len(self.datapoints)

def yn_to_bool(x: str) -> bool:
  return True if x.lower() == 'y' else False

def parse_course_rating_data_set(filename: str) -> LabelledDataSet:
  f = open(filename, 'r')
  line1 = f.readline().rstrip()
  columns = line1.split(' ')
  features = columns[1:]

  if columns[0] != 'Rating':
    # TODO: throw error
    pass

  datapoints = []
  for line in f.readlines():
    values = line.rstrip().split(' ')
    parsed_feature_values = list(map(yn_to_bool, values[1:]))
    datapoints.append(LabelledDatapoint(parsed_feature_values, values[0]))

  return LabelledDataSet(features, datapoints)


def print_labelled_dataset(ds: LabelledDataSet):
  print(ds.get_feature_names())
  for i in range(ds.size()):
    print(" {0:>2} |".format(ds.get_label(i)), end="")
    fv_display = map(lambda fv: '1' if fv == True else '0', ds.get_feature_values(i))
    print(" " + ' '.join(fv_display))


if __name__ == '__main__':
  dataset1 = parse_course_rating_data_set("ciml-course-rating-data-set.txt")
  # print the ingested dataset
  print_labelled_dataset(dataset1)

  gte0 = lambda l: l == '0' or l == '+1' or l == '+2'

  def print_feat_val_hist(i: int, feat_val: bool) -> None:
    filtered = dataset1.filter(lambda dp: dp.get_feature_value(i) == feat_val)
    total_filtered = filtered.size()
    # number of datapoints whose label is in {0, +1, +2}
    amt_liked = filtered.count_label_predicate(gte0)
    # count_f1_y_dislike = filter_f1_y.count_label_predicate(lt0)
    amt_disliked = total_filtered - amt_liked
    print(f"= {'y' if feat_val else 'n'} [{amt_liked}, {amt_disliked}]")

  # compute like/dislike histograms along each feature
  def print_histograms_for_feature(i: int):
    print(f"f{i+1}: {dataset1.get_feature_names()[i]}")
    print_feat_val_hist(i, True)
    print_feat_val_hist(i, False)

  for i in range(5):
    print_histograms_for_feature(i)
