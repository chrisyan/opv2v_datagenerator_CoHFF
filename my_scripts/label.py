from collections import namedtuple
'''
platte for carla 0.9.13
total 26 classes = unlabeled + 25 classes
'''
#--------------------------------------------------------------------------------
# Definitions
#--------------------------------------------------------------------------------

# a label and all meta information
Label = namedtuple( 'Label' , [

    'name'        , # The identifier of this label, e.g. 'car', 'person', ... .
                    # We use them to uniquely name a class

    'id'          , # An integer ID that is associated with this label.
                    # The IDs are used to represent the label in ground truth images
                    # An ID of -1 means that this label does not have an ID and thus
                    # is ignored when creating ground truth images (e.g. license plate).
                    # Do not modify these IDs, since exactly these IDs are expected by the
                    # evaluation server.

    'trainId'     , # Feel free to modify these IDs as suitable for your method. Then create
                    # ground truth images with train IDs, using the tools provided in the
                    # 'preparation' folder. However, make sure to validate or submit results
                    # to our evaluation server using the regular IDs above!
                    # For trainIds, multiple labels might have the same ID. Then, these labels
                    # are mapped to the same class in the ground truth images. For the inverse
                    # mapping, we use the label that is defined first in the list below.
                    # For example, mapping all void-type classes to the same ID in training,
                    # might make sense for some approaches.
                    # Max value is 255!

    'category'    , # The name of the category that this label belongs to

    'categoryId'  , # The ID of this category. Used to create ground truth images
                    # on category level.

    'hasInstances', # Whether this label distinguishes between single instances or not

    'ignoreInEval', # Whether pixels having this class as ground truth label are ignored
                    # during evaluations or not

    'color'       , # The color of this label
    ] )


#--------------------------------------------------------------------------------
# A list of all labels
#--------------------------------------------------------------------------------

# Please adapt the train IDs as appropriate for you approach.
# Note that you might want to ignore labels with ID 255 during training.
# Further note that the current train IDs are only a suggestion. You can use whatever you like.
# Make sure to provide your results using the original IDs and not the training IDs.
# Note that many IDs are ignored in evaluation and thus you never need to predict these!

labels = [
    #       name                     id    trainId   category            catId     hasInstances   ignoreInEval   color
    Label(  'Unalbeled'            ,  7 ,        0 , 'flat'            , 1       , False        , False        , (0, 0, 0) ),
    Label(  'Building'             ,  8 ,        1 , 'flat'            , 1       , False        , False        , (70, 70, 70) ),
    Label(  'Fence'                , 11 ,        2 , 'construction'    , 2       , False        , False        , (100, 40, 40) ),
    Label(  'Other'                , 12 ,        3 , 'construction'    , 2       , False        , False        , (55, 90, 80) ),
    Label(  'Pedestrian'           , 13 ,        4 , 'construction'    , 2       , False        , False        , (220, 20, 60) ),
    Label(  'Pole'                 , 17 ,        5 , 'object'          , 3       , False        , False        , (153, 153, 153) ),
    Label(  'RoadLine'             , 19 ,        6 , 'object'          , 3       , False        , False        , (157, 234, 50) ),
    Label(  'Road'                 , 20 ,        7 , 'object'          , 3       , False        , False        , (128, 64, 128) ),
    Label(  'SideWalk'             , 21 ,        8 , 'nature'          , 4       , False        , False        , (244, 35, 232) ),
    Label(  'Vegetation'           , 22 ,        9 , 'nature'          , 4       , False        , False        , (107, 142, 35) ),
    Label(  'Vehicles'             , 23 ,       10 , 'sky'             , 5       , False        , False        , (0, 0, 142) ),
    Label(  'Wall'                 , 24 ,       11 , 'human'           , 6       , True         , False        , (102, 102, 156) ),
    Label(  'TrafficSign'          , 25 ,       12 , 'human'           , 6       , True         , False        , (220, 220, 0) ),
    Label(  'Sky'                  , 26 ,       13 , 'vehicle'         , 7       , True         , False        , (70, 130, 180) ),
    Label(  'Ground'               , 27 ,       14 , 'vehicle'         , 7       , True         , False        , (81, 0, 81) ),
    Label(  'Bridge'               , 28 ,       15 , 'vehicle'         , 7       , True         , False        , (150, 100, 100) ),
    Label(  'RailTrack'            , 31 ,       16 , 'vehicle'         , 7       , True         , False        , (230, 150, 140) ),
    Label(  'GuardRail'            , 32 ,       17 , 'vehicle'         , 7       , True         , False        , (180, 165, 180) ),
    Label(  'TrafficLight'         , 33 ,       18 , 'vehicle'         , 7       , True         , False        , (250, 170, 30) ),
    Label(  'Static'               , 33 ,       19 , 'vehicle'         , 7       , True         , False        , (110, 190, 160) ),
    Label(  'Dynamic'              , 33 ,       20 , 'vehicle'         , 7       , True         , False        , (170, 120, 50) ),
    Label(  'Water'                , 33 ,       21 , 'vehicle'         , 7       , True         , False        , (45, 60, 150) ),
    Label(  'Terrain'              , 33 ,       22 , 'vehicle'         , 7       , True         , False        , (145, 170, 100) ),
    Label(  'ReflectorPost'        , 33 ,       23 , 'vehicle'         , 7       , True         , False        , (255, 51, 51) ),
    Label(  'Barrier'              , 33 ,       24 , 'vehicle'         , 7       , True         , False        , (255, 255, 0) ),
    Label(  'TrafficCone'          , 33 ,       25 , 'vehicle'         , 7       , True         , False        , (0, 255, 0) ),
    Label('ReflectorPost', 33, 26, 'vehicle', 7, True, False, (255, 51, 51)),
    Label('Barrier', 33, 27, 'vehicle', 7, True, False, (255, 255, 0)),
    Label('TrafficCone', 28, 25, 'vehicle', 7, True, False, (0, 255, 0)),
    Label('ReflectorPost', 33, 29, 'vehicle', 7, True, False, (255, 51, 51)),
    Label('Barrier', 33, 30, 'vehicle', 7, True, False, (255, 255, 0)),
    Label('TrafficCone', 33, 31, 'vehicle', 7, True, False, (0, 255, 0))
]


#--------------------------------------------------------------------------------
# Create dictionaries for a fast lookup
#--------------------------------------------------------------------------------

# Please refer to the main method below for example usages!

# name to label object
name2label      = { label.name    : label for label in labels           }
# id to label object
id2label        = { label.id      : label for label in labels           }
# trainId to label object
trainId2label   = { label.trainId : label for label in reversed(labels) }
# category to list of label objects
category2labels = {}
for label in labels:
    category = label.category
    if category in category2labels:
        category2labels[category].append(label)
    else:
        category2labels[category] = [label]

#--------------------------------------------------------------------------------
# Main for testing
#--------------------------------------------------------------------------------

# just a dummy main
if __name__ == "__main__":
    # Print all the labels
    print("List of cityscapes labels:")
    print("")
    print("    {:>21} | {:>3} | {:>7} | {:>14} | {:>10} | {:>12} | {:>12}".format( 'name', 'id', 'trainId', 'category', 'categoryId', 'hasInstances', 'ignoreInEval' ))
    print("    " + ('-' * 98))
    for label in labels:
        # print("    {:>21} | {:>3} | {:>7} | {:>14} | {:>10} | {:>12} | {:>12}".format( label.name, label.id, label.trainId, label.category, label.categoryId, label.hasInstances, label.ignoreInEval ))
        print(" \"{:}\"".format(label.name))
    print("")

    print("Example usages:")

    # Map from name to label
    name = 'car'
    id   = name2label[name].id
    print("ID of label '{name}': {id}".format( name=name, id=id ))

    # Map from ID to label
    category = id2label[id].category
    print("Category of label with ID '{id}': {category}".format( id=id, category=category ))

    # Map from trainID to label
    trainId = 0
    name = trainId2label[trainId].name
    print("Name of label with trainID '{id}': {name}".format( id=trainId, name=name ))
