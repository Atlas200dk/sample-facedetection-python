# constants
# if you want change the .so please make it
# I put the face_detection_post_process in the sample path and run deploy.sh, and copy .co from facedetectionapp/out
# face box color
kFaceBoxColorR = 255  # int8.
kFaceBoxColorG = 190
kFaceBoxColorB = 0

# face box border width
kFaceBoxBorderWidth = 2  # int

# face label color
kFaceLabelColorR = 255  # int8.
kFaceLabelColorG = 255
kFaceLabelColorB = 0

# face label font
kFaceLabelFontSize = 0.7  # double
kFaceLabelFontWidth = 2  # int

# face label text prefix
kFaceLabelTextPrefix = 'Face:'
kFaceLabelTextSuffix = '%'
# $$ parameters for drawing box and label end $$

# port number range
kPortMinNumber = 0  # int.
kPortMaxNumber = 65535

# confidence range
kConfidenceMin = 0.0  # doulbe.
kConfidenceMax = 1.0

# face detection function return value
kFdFunSuccess = 0  # int32.
kFdFunFailed = -1

# need to deal results when index is 2
kDealResultIndex = 2

# each results size
kEachResultSize = 7

# attribute index
kAttributeIndex = 1

# score index
kScoreIndex = 2

# anchor_lt.x index
kAnchorLeftTopAxisIndexX = 3

# anchor_lt.y index
kAnchorLeftTopAxisIndexY = 4

# anchor_rb.x index
kAnchorRightBottomAxisIndexX = 5

# anchor_rb.y index
kAnchorRightBottomAxisIndexY = 6

# face attribute
kAttributeFaceLabelValue = 1.0  # float.
kAttributeFaceDeviation = 0.00001

# percent
kScorePercent = 100  # int32

# IP regular expression
kIpRegularExpression = "^((25[0-5]|2[0-4]\\d|[1]{1}\\d{1}\\d{1}|[1-9]{1}\\d{1}|\\d{1})($|(?!\\.$)\\.)){4}$"

# channel name regular expression
kChannelNameRegularExpression = "[a-zA-Z0-9/]+"

HIAI_ERROR = 3  # from cpp value. if you want to it accord with control, please amend it
HIAI_OK = 0