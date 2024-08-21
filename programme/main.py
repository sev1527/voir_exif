# -*- coding: utf-8 -*-
"""
Programme créé par sev1527.
Page d'accueil du dépôt github :
    https://github.com/sev1527/voir_exif

Source pour l'interprétation des données EXIF :
    https://exiv2.org/tags.html
"""

from PIL import Image
from tkinter import Tk, Toplevel, Frame, Label, Button
from tkinter.ttk import Treeview, Scrollbar
from tkinter.filedialog import askopenfilename, asksaveasfilename
import webbrowser


VERSION = "1.1"

NOMS = {
    11: ['Exif.Image.ProcessingSoftware', 'Ascii', 'The name and version of the software used to post-process the picture.'],
    254: ['Exif.Image.NewSubfileType', 'Long', 'A general indication of the kind of data contained in this subfile.'],
    255: ['Exif.Image.SubfileType', 'Short', 'A general indication of the kind of data contained in this subfile. This field is deprecated. The NewSubfileType field should be used instead.'],
    256: ['Exif.Image.ImageWidth', 'Long', 'The number of columns of image data, equal to the number of pixels per row. In JPEG compressed data a JPEG marker is used instead of this tag.'],
    257: ['Exif.Image.ImageLength', 'Long', 'The number of rows of image data. In JPEG compressed data a JPEG marker is used instead of this tag.'],
    258: ['Exif.Image.BitsPerSample', 'Short', 'The number of bits per image component. In this standard each component of the image is 8 bits, so the value for this tag is 8. See also <SamplesPerPixel>. In JPEG compressed data a JPEG marker is used instead of this tag.'],
    259: ['Exif.Image.Compression', 'Short', 'The compression scheme used for the image data. When a primary image is JPEG compressed, this designation is not necessary and is omitted. When thumbnails use JPEG compression, this tag value is set to 6.'],
    262: ['Exif.Image.PhotometricInterpretation', 'Short', 'The pixel composition. In JPEG compressed data a JPEG marker is used instead of this tag.'],
    263: ['Exif.Image.Thresholding', 'Short', 'For black and white TIFF files that represent shades of gray, the technique used to convert from gray to black and white pixels.'],
    264: ['Exif.Image.CellWidth', 'Short', 'The width of the dithering or halftoning matrix used to create a dithered or halftoned bilevel file.'],
    265: ['Exif.Image.CellLength', 'Short', 'The length of the dithering or halftoning matrix used to create a dithered or halftoned bilevel file.'],
    266: ['Exif.Image.FillOrder', 'Short', 'The logical order of bits within a byte'],
    269: ['Exif.Image.DocumentName', 'Ascii', 'The name of the document from which this image was scanned.'],
    270: ['Exif.Image.ImageDescription', 'Ascii', 'A character string giving the title of the image. It may be a comment such as "1988 company picnic" or the like. Two-bytes character codes cannot be used. When a 2-bytes code is necessary, the Exif Private tag <UserComment> is to be used.'],
    271: ['Exif.Image.Make', 'Ascii', 'The manufacturer of the recording equipment. This is the manufacturer of the DSC, scanner, video digitizer or other equipment that generated the image. When the field is left blank, it is treated as unknown.'],
    272: ['Exif.Image.Model', 'Ascii', 'The model name or model number of the equipment. This is the model name or number of the DSC, scanner, video digitizer or other equipment that generated the image. When the field is left blank, it is treated as unknown.'],
    273: ['Exif.Image.StripOffsets', 'Long', 'For each strip, the byte offset of that strip. It is recommended that this be selected so the number of strip bytes does not exceed 64 Kbytes. With JPEG compressed data this designation is not needed and is omitted. See also <RowsPerStrip> and <StripByteCounts>.'],
    274: ['Exif.Image.Orientation', 'Short', 'The image orientation viewed in terms of rows and columns.'],
    277: ['Exif.Image.SamplesPerPixel', 'Short', 'The number of components per pixel. Since this standard applies to RGB and YCbCr images, the value set for this tag is 3. In JPEG compressed data a JPEG marker is used instead of this tag.'],
    278: ['Exif.Image.RowsPerStrip', 'Long', 'The number of rows per strip. This is the number of rows in the image of one strip when an image is divided into strips. With JPEG compressed data this designation is not needed and is omitted. See also <StripOffsets> and <StripByteCounts>.'],
    279: ['Exif.Image.StripByteCounts', 'Long', 'The total number of bytes in each strip. With JPEG compressed data this designation is not needed and is omitted.'],
    282: ['Exif.Image.XResolution', 'Rational', 'The number of pixels per <ResolutionUnit> in the <ImageWidth> direction. When the image resolution is unknown, 72 [dpi] is designated.'],
    283: ['Exif.Image.YResolution', 'Rational', 'The number of pixels per <ResolutionUnit> in the <ImageLength> direction. The same value as <XResolution> is designated.'],
    284: ['Exif.Image.PlanarConfiguration', 'Short', 'Indicates whether pixel components are recorded in a chunky or planar format. In JPEG compressed files a JPEG marker is used instead of this tag. If this field does not exist, the TIFF default of 1 (chunky) is assumed.'],
    285: ['Exif.Image.PageName', 'Ascii', 'The name of the page from which this image was scanned.'],
    286: ['Exif.Image.XPosition', 'Rational', 'X position of the image. The X offset in ResolutionUnits of the left side of the image, with respect to the left side of the page.'],
    287: ['Exif.Image.YPosition', 'Rational', 'Y position of the image. The Y offset in ResolutionUnits of the top of the image, with respect to the top of the page. In the TIFF coordinate scheme, the positive Y direction is down, so that YPosition is always positive.'],
    290: ['Exif.Image.GrayResponseUnit', 'Short', 'The precision of the information contained in the GrayResponseCurve.'],
    291: ['Exif.Image.GrayResponseCurve', 'Short', 'For grayscale data, the optical density of each possible pixel value.'],
    292: ['Exif.Image.T4Options', 'Long', 'T.4-encoding options.'],
    293: ['Exif.Image.T6Options', 'Long', 'T.6-encoding options.'],
    296: ['Exif.Image.ResolutionUnit', 'Short', 'The unit for measuring <XResolution> and <YResolution>. The same unit is used for both <XResolution> and <YResolution>. If the image resolution is unknown, 2 (inches) is designated.'],
    297: ['Exif.Image.PageNumber', 'Short', 'The page number of the page from which this image was scanned.'],
    301: ['Exif.Image.TransferFunction', 'Short', 'A transfer function for the image, described in tabular style. Normally this tag is not necessary, since color space is specified in the color space information tag (<ColorSpace>).'],
    305: ['Exif.Image.Software', 'Ascii', 'This tag records the name and version of the software or firmware of the camera or image input device used to generate the image. The detailed format is not specified, but it is recommended that the example shown below be followed. When the field is left blank, it is treated as unknown.'],
    306: ['Exif.Image.DateTime', 'Ascii', 'The date and time of image creation. In Exif standard, it is the date and time the file was changed.'],
    315: ['Exif.Image.Artist', 'Ascii', 'This tag records the name of the camera owner, photographer or image creator. The detailed format is not specified, but it is recommended that the information be written as in the example below for ease of Interoperability. When the field is left blank, it is treated as unknown. Ex.) "Camera owner, John Smith; Photographer, Michael Brown; Image creator, Ken James"'],
    316: ['Exif.Image.HostComputer', 'Ascii', 'This tag records information about the host computer used to generate the image.'],
    317: ['Exif.Image.Predictor', 'Short', 'A predictor is a mathematical operator that is applied to the image data before an encoding scheme is applied.'],
    318: ['Exif.Image.WhitePoint', 'Rational', 'The chromaticity of the white point of the image. Normally this tag is not necessary, since color space is specified in the colorspace information tag (<ColorSpace>).'],
    319: ['Exif.Image.PrimaryChromaticities', 'Rational', 'The chromaticity of the three primary colors of the image. Normally this tag is not necessary, since colorspace is specified in the colorspace information tag (<ColorSpace>).'],
    320: ['Exif.Image.ColorMap', 'Short', 'A color map for palette color images. This field defines a Red-Green-Blue color map (often called a lookup table) for palette-color images. In a palette-color image, a pixel value is used to index into an RGB lookup table.'],
    321: ['Exif.Image.HalftoneHints', 'Short', 'The purpose of the HalftoneHints field is to convey to the halftone function the range of gray levels within a colorimetrically-specified image that should retain tonal detail.'],
    322: ['Exif.Image.TileWidth', 'Long', 'The tile width in pixels. This is the number of columns in each tile.'],
    323: ['Exif.Image.TileLength', 'Long', 'The tile length (height) in pixels. This is the number of rows in each tile.'],
    324: ['Exif.Image.TileOffsets', 'Short', 'For each tile, the byte offset of that tile, as compressed and stored on disk. The offset is specified with respect to the beginning of the TIFF file. Note that this implies that each tile has a location independent of the locations of other tiles.'],
    325: ['Exif.Image.TileByteCounts', 'Long', 'For each tile, the number of (compressed) bytes in that tile. See TileOffsets for a description of how the byte counts are ordered.'],
    330: ['Exif.Image.SubIFDs', 'Long', 'Defined by Adobe Corporation to enable TIFF Trees within a TIFF file.'],
    332: ['Exif.Image.InkSet', 'Short', 'The set of inks used in a separated (PhotometricInterpretation=5) image.'],
    333: ['Exif.Image.InkNames', 'Ascii', 'The name of each ink used in a separated (PhotometricInterpretation=5) image.'],
    334: ['Exif.Image.NumberOfInks', 'Short', 'The number of inks. Usually equal to SamplesPerPixel, unless there are extra samples.'],
    336: ['Exif.Image.DotRange', 'Byte', 'The component values that correspond to a 0% dot and 100% dot.'],
    337: ['Exif.Image.TargetPrinter', 'Ascii', 'A description of the printing environment for which this separation is intended.'],
    338: ['Exif.Image.ExtraSamples', 'Short', 'Specifies that each pixel has m extra components whose interpretation is defined by one of the values listed below.'],
    339: ['Exif.Image.SampleFormat', 'Short', 'This field specifies how to interpret each data sample in a pixel.'],
    340: ['Exif.Image.SMinSampleValue', 'Short', 'This field specifies the minimum sample value.'],
    341: ['Exif.Image.SMaxSampleValue', 'Short', 'This field specifies the maximum sample value.'],
    342: ['Exif.Image.TransferRange', 'Short', 'Expands the range of the TransferFunction'],
    343: ['Exif.Image.ClipPath', 'Byte', "A TIFF ClipPath is intended to mirror the essentials of PostScript's path creation functionality."],
    344: ['Exif.Image.XClipPathUnits', 'SShort', 'The number of units that span the width of the image, in terms of integer ClipPath coordinates.'],
    345: ['Exif.Image.YClipPathUnits', 'SShort', 'The number of units that span the height of the image, in terms of integer ClipPath coordinates.'],
    346: ['Exif.Image.Indexed', 'Short', "Indexed images are images where the 'pixels' do not represent color values, but rather an index (usually 8-bit) into a separate color table, the ColorMap."],
    347: ['Exif.Image.JPEGTables', 'Undefined', 'This optional tag may be used to encode the JPEG quantization and Huffman tables for subsequent use by the JPEG decompression process.'],
    351: ['Exif.Image.OPIProxy', 'Short', 'OPIProxy gives information concerning whether this image is a low-resolution proxy of a high-resolution image (Adobe OPI).'],
    512: ['Exif.Image.JPEGProc', 'Long', 'This field indicates the process used to produce the compressed data'],
    513: ['Exif.Image.JPEGInterchangeFormat', 'Long', 'The offset to the start byte (SOI) of JPEG compressed thumbnail data. This is not used for primary image JPEG data.'],
    514: ['Exif.Image.JPEGInterchangeFormatLength', 'Long', 'The number of bytes of JPEG compressed thumbnail data. This is not used for primary image JPEG data. JPEG thumbnails are not divided but are recorded as a continuous JPEG bitstream from SOI to EOI. Appn and COM markers should not be recorded. Compressed thumbnails must be recorded in no more than 64 Kbytes, including all other data to be recorded in APP1.'],
    515: ['Exif.Image.JPEGRestartInterval', 'Short', 'This Field indicates the length of the restart interval used in the compressed image data.'],
    517: ['Exif.Image.JPEGLosslessPredictors', 'Short', 'This Field points to a list of lossless predictor-selection values, one per component.'],
    518: ['Exif.Image.JPEGPointTransforms', 'Short', 'This Field points to a list of point transform values, one per component.'],
    519: ['Exif.Image.JPEGQTables', 'Long', 'This Field points to a list of offsets to the quantization tables, one per component.'],
    520: ['Exif.Image.JPEGDCTables', 'Long', 'This Field points to a list of offsets to the DC Huffman tables or the lossless Huffman tables, one per component.'],
    521: ['Exif.Image.JPEGACTables', 'Long', 'This Field points to a list of offsets to the Huffman AC tables, one per component.'],
    529: ['Exif.Image.YCbCrCoefficients', 'Rational', 'The matrix coefficients for transformation from RGB to YCbCr image data. No default is given in TIFF; but here the value given in Appendix E, "Color Space Guidelines", is used as the default. The color space is declared in a color space information tag, with the default being the value that gives the optimal image characteristics Interoperability this condition.'],
    530: ['Exif.Image.YCbCrSubSampling', 'Short', 'The sampling ratio of chrominance components in relation to the luminance component. In JPEG compressed data a JPEG marker is used instead of this tag.'],
    531: ['Exif.Image.YCbCrPositioning', 'Short', 'The position of chrominance components in relation to the luminance component. This field is designated only for JPEG compressed data or uncompressed YCbCr data. The TIFF default is 1 (centered); but when Y:Cb:Cr = 4:2:2 it is recommended in this standard that 2 (co-sited) be used to record data, in order to improve the image quality when viewed on TV systems. When this field does not exist, the reader shall assume the TIFF default. In the case of Y:Cb:Cr = 4:2:0, the TIFF default (centered) is recommended. If the reader does not have the capability of supporting both kinds of <YCbCrPositioning>, it shall follow the TIFF default regardless of the value in this field. It is preferable that readers be able to support both centered and co-sited positioning.'],
    532: ['Exif.Image.ReferenceBlackWhite', 'Rational', 'The reference black point value and reference white point value. No defaults are given in TIFF, but the values below are given as defaults here. The color space is declared in a color space information tag, with the default being the value that gives the optimal image characteristics Interoperability these conditions.'],
    700: ['Exif.Image.XMLPacket', 'Byte', 'XMP Metadata (Adobe technote 9-14-02)'],
    18246: ['Exif.Image.Rating', 'Short', 'Rating tag used by Windows'],
    18249: ['Exif.Image.RatingPercent', 'Short', 'Rating tag used by Windows, value in percent'],
    28722: ['Exif.Image.VignettingCorrParams', 'SShort', 'Sony vignetting correction parameters'],
    28725: ['Exif.Image.ChromaticAberrationCorrParams', 'SShort', 'Sony chromatic aberration correction parameters'],
    28727: ['Exif.Image.DistortionCorrParams', 'SShort', 'Sony distortion correction parameters'],
    32781: ['Exif.Image.ImageID', 'Ascii', 'ImageID is the full pathname of the original, high-resolution image, or any other identifying string that uniquely identifies the original image (Adobe OPI).'],
    33421: ['Exif.Image.CFARepeatPatternDim', 'Short', 'Contains two values representing the minimum rows and columns to define the repeating patterns of the color filter array'],
    33422: ['Exif.Image.CFAPattern', 'Byte', 'Indicates the color filter array (CFA) geometric pattern of the image sensor when a one-chip color area sensor is used. It does not apply to all sensing methods'],
    33423: ['Exif.Image.BatteryLevel', 'Rational', 'Contains a value of the battery level as a fraction or string'],
    33432: ['Exif.Image.Copyright', 'Ascii', 'Copyright information. In this standard the tag is used to indicate both the photographer and editor copyrights. It is the copyright notice of the person or organization claiming rights to the image. The Interoperability copyright statement including date and rights should be written in this field; e.g., "Copyright, John Smith, 19xx. All rights reserved.". In this standard the field records both the photographer and editor copyrights, with each recorded in a separate part of the statement. When there is a clear distinction between the photographer and editor copyrights, these are to be written in the order of photographer followed by editor copyright, separated by NULL (in this case since the statement also ends with a NULL, there are two NULL codes). When only the photographer copyright is given, it is terminated by one NULL code. When only the editor copyright is given, the photographer copyright part consists of one space followed by a terminating NULL code, then the editor copyright is given. When the field is left blank, it is treated as unknown.'],
    33434: ['Exif.Image.ExposureTime', 'Rational', 'Exposure time, given in seconds.'],
    33437: ['Exif.Image.FNumber', 'Rational', 'The F number.'],
    33723: ['Exif.Image.IPTCNAA', 'Long', 'Contains an IPTC/NAA record'],
    34377: ['Exif.Image.ImageResources', 'Byte', 'Contains information embedded by the Adobe Photoshop application'],
    34665: ['Exif.Image.ExifTag', 'Long', 'A pointer to the Exif IFD. Interoperability, Exif IFD has the same structure as that of the IFD specified in TIFF. ordinarily, however, it does not contain image data as in the case of TIFF.'],
    34675: ['Exif.Image.InterColorProfile', 'Undefined', 'Contains an InterColor Consortium (ICC) format color space characterization/profile'],
    34850: ['Exif.Image.ExposureProgram', 'Short', 'The class of the program used by the camera to set exposure when the picture is taken.'],
    34852: ['Exif.Image.SpectralSensitivity', 'Ascii', 'Indicates the spectral sensitivity of each channel of the camera used.'],
    34853: ['Exif.Image.GPSTag', 'Long', 'A pointer to the GPS Info IFD. The Interoperability structure of the GPS Info IFD, like that of Exif IFD, has no image data.'],
    34855: ['Exif.Image.ISOSpeedRatings', 'Short', 'Indicates the ISO Speed and ISO Latitude of the camera or input device as specified in ISO 12232.'],
    34856: ['Exif.Image.OECF', 'Undefined', 'Indicates the Opto-Electric Conversion Function (OECF) specified in ISO 14524.'],
    34857: ['Exif.Image.Interlace', 'Short', 'Indicates the field number of multifield images.'],
    34858: ['Exif.Image.TimeZoneOffset', 'SShort', 'This optional tag encodes the time zone of the camera clock (relative to Greenwich Mean Time) used to create the DataTimeOriginal tag-value when the picture was taken. It may also contain the time zone offset of the clock used to create the DateTime tag-value when the image was modified.'],
    34859: ['Exif.Image.SelfTimerMode', 'Short', 'Number of seconds image capture was delayed from button press.'],
    36867: ['Exif.Image.DateTimeOriginal', 'Ascii', 'The date and time when the original image data was generated.'],
    37122: ['Exif.Image.CompressedBitsPerPixel', 'Rational', 'Specific to compressed data; states the compressed bits per pixel.'],
    37377: ['Exif.Image.ShutterSpeedValue', 'SRational', 'Shutter speed.'],
    37378: ['Exif.Image.ApertureValue', 'Rational', 'The lens aperture.'],
    37379: ['Exif.Image.BrightnessValue', 'SRational', 'The value of brightness.'],
    37380: ['Exif.Image.ExposureBiasValue', 'SRational', 'The exposure bias.'],
    37381: ['Exif.Image.MaxApertureValue', 'Rational', 'The smallest F number of the lens.'],
    37382: ['Exif.Image.SubjectDistance', 'SRational', 'The distance to the subject, given in meters.'],
    37383: ['Exif.Image.MeteringMode', 'Short', 'The metering mode.'],
    37384: ['Exif.Image.LightSource', 'Short', 'The kind of light source.'],
    37385: ['Exif.Image.Flash', 'Short', 'Indicates the status of flash when the image was shot.'],
    37386: ['Exif.Image.FocalLength', 'Rational', 'The actual focal length of the lens, in mm.'],
    37387: ['Exif.Image.FlashEnergy', 'Rational', 'Amount of flash energy (BCPS).'],
    37388: ['Exif.Image.SpatialFrequencyResponse', 'Undefined', 'SFR of the camera.'],
    37389: ['Exif.Image.Noise', 'Undefined', 'Noise measurement values.'],
    37390: ['Exif.Image.FocalPlaneXResolution', 'Rational', 'Number of pixels per FocalPlaneResolutionUnit (37392) in ImageWidth direction for main image.'],
    37391: ['Exif.Image.FocalPlaneYResolution', 'Rational', 'Number of pixels per FocalPlaneResolutionUnit (37392) in ImageLength direction for main image.'],
    37392: ['Exif.Image.FocalPlaneResolutionUnit', 'Short', 'Unit of measurement for FocalPlaneXResolution(37390) and FocalPlaneYResolution(37391).'],
    37393: ['Exif.Image.ImageNumber', 'Long', 'Number assigned to an image, e.g., in a chained image burst.'],
    37394: ['Exif.Image.SecurityClassification', 'Ascii', 'Security classification assigned to the image.'],
    37395: ['Exif.Image.ImageHistory', 'Ascii', 'Record of what has been done to the image.'],
    37396: ['Exif.Image.SubjectLocation', 'Short', 'Indicates the location and area of the main subject in the overall scene.'],
    37397: ['Exif.Image.ExposureIndex', 'Rational', 'Encodes the camera exposure index setting when image was captured.'],
    37398: ['Exif.Image.TIFFEPStandardID', 'Byte', "Contains four ASCII characters representing the TIFF/EP standard version of a TIFF/EP file, eg '1', '0', '0', '0'"],
    37399: ['Exif.Image.SensingMethod', 'Short', 'Type of image sensor.'],
    40091: ['Exif.Image.XPTitle', 'Byte', 'Title tag used by Windows, encoded in UCS2'],
    40092: ['Exif.Image.XPComment', 'Byte', 'Comment tag used by Windows, encoded in UCS2'],
    40093: ['Exif.Image.XPAuthor', 'Byte', 'Author tag used by Windows, encoded in UCS2'],
    40094: ['Exif.Image.XPKeywords', 'Byte', 'Keywords tag used by Windows, encoded in UCS2'],
    40095: ['Exif.Image.XPSubject', 'Byte', 'Subject tag used by Windows, encoded in UCS2'],
    50341: ['Exif.Image.PrintImageMatching', 'Undefined', 'Print Image Matching, description needed.'],
    50706: ['Exif.Image.DNGVersion', 'Byte', 'This tag encodes the DNG four-tier version number. For files compliant with version 1.1.0.0 of the DNG specification, this tag should contain the bytes: 1, 1, 0, 0.'],
    50707: ['Exif.Image.DNGBackwardVersion', 'Byte', 'This tag specifies the oldest version of the Digital Negative specification for which a file is compatible. Readers shouldnot attempt to read a file if this tag specifies a version number that is higher than the version number of the specification the reader was based on. In addition to checking the version tags, readers should, for all tags, check the types, counts, and values, to verify it is able to correctly read the file.'],
    50708: ['Exif.Image.UniqueCameraModel', 'Ascii', "Defines a unique, non-localized name for the camera model that created the image in the raw file. This name should include the manufacturer's name to avoid conflicts, and should not be localized, even if the camera name itself is localized for different markets (see LocalizedCameraModel). This string may be used by reader software to index into per-model preferences and replacement profiles."],
    50709: ['Exif.Image.LocalizedCameraModel', 'Byte', 'Similar to the UniqueCameraModel field, except the name can be localized for different markets to match the localization of the camera name.'],
    50710: ['Exif.Image.CFAPlaneColor', 'Byte', 'Provides a mapping between the values in the CFAPattern tag and the plane numbers in LinearRaw space. This is a required tag for non-RGB CFA images.'],
    50711: ['Exif.Image.CFALayout', 'Short', 'Describes the spatial layout of the CFA.'],
    50712: ['Exif.Image.LinearizationTable', 'Short', 'Describes a lookup table that maps stored values into linear values. This tag is typically used to increase compression ratios by storing the raw data in a non-linear, more visually uniform space with fewer total encoding levels. If SamplesPerPixel is not equal to one, this single table applies to all the samples for each pixel.'],
    50713: ['Exif.Image.BlackLevelRepeatDim', 'Short', 'Specifies repeat pattern size for the BlackLevel tag.'],
    50714: ['Exif.Image.BlackLevel', 'Rational', 'Specifies the zero light (a.k.a. thermal black or black current) encoding level, as a repeating pattern. The origin of this pattern is the top-left corner of the ActiveArea rectangle. The values are stored in row-column-sample scan order.'],
    50715: ['Exif.Image.BlackLevelDeltaH', 'SRational', 'If the zero light encoding level is a function of the image column, BlackLevelDeltaH specifies the difference between the zero light encoding level for each column and the baseline zero light encoding level. If SamplesPerPixel is not equal to one, this single table applies to all the samples for each pixel.'],
    50716: ['Exif.Image.BlackLevelDeltaV', 'SRational', 'If the zero light encoding level is a function of the image row, this tag specifies the difference between the zero light encoding level for each row and the baseline zero light encoding level. If SamplesPerPixel is not equal to one, this single table applies to all the samples for each pixel.'],
    50717: ['Exif.Image.WhiteLevel', 'Long', "This tag specifies the fully saturated encoding level for the raw sample values. Saturation is caused either by the sensor itself becoming highly non-linear in response, or by the camera's analog to digital converter clipping."],
    50718: ['Exif.Image.DefaultScale', 'Rational', 'DefaultScale is required for cameras with non-square pixels. It specifies the default scale factors for each direction to convert the image to square pixels. Typically these factors are selected to approximately preserve total pixel count. For CFA images that use CFALayout equal to 2, 3, 4, or 5, such as the Fujifilm SuperCCD, these two values should usually differ by a factor of 2.0.'],
    50719: ['Exif.Image.DefaultCropOrigin', 'Long', 'Raw images often store extra pixels around the edges of the final image. These extra pixels help prevent interpolation artifacts near the edges of the final image. DefaultCropOrigin specifies the origin of the final image area, in raw image coordinates (i.e., before the DefaultScale has been applied), relative to the top-left corner of the ActiveArea rectangle.'],
    50720: ['Exif.Image.DefaultCropSize', 'Long', 'Raw images often store extra pixels around the edges of the final image. These extra pixels help prevent interpolation artifacts near the edges of the final image. DefaultCropSize specifies the size of the final image area, in raw image coordinates (i.e., before the DefaultScale has been applied).'],
    50721: ['Exif.Image.ColorMatrix1', 'SRational', 'ColorMatrix1 defines a transformation matrix that converts XYZ values to reference camera native color space values, under the first calibration illuminant. The matrix values are stored in row scan order. The ColorMatrix1 tag is required for all non-monochrome DNG files.'],
    50722: ['Exif.Image.ColorMatrix2', 'SRational', 'ColorMatrix2 defines a transformation matrix that converts XYZ values to reference camera native color space values, under the second calibration illuminant. The matrix values are stored in row scan order.'],
    50723: ['Exif.Image.CameraCalibration1', 'SRational', 'CameraCalibration1 defines a calibration matrix that transforms reference camera native space values to individual camera native space values under the first calibration illuminant. The matrix is stored in row scan order. This matrix is stored separately from the matrix specified by the ColorMatrix1 tag to allow raw converters to swap in replacement color matrices based on UniqueCameraModel tag, while still taking advantage of any per-individual camera calibration performed by the camera manufacturer.'],
    50724: ['Exif.Image.CameraCalibration2', 'SRational', 'CameraCalibration2 defines a calibration matrix that transforms reference camera native space values to individual camera native space values under the second calibration illuminant. The matrix is stored in row scan order. This matrix is stored separately from the matrix specified by the ColorMatrix2 tag to allow raw converters to swap in replacement color matrices based on UniqueCameraModel tag, while still taking advantage of any per-individual camera calibration performed by the camera manufacturer.'],
    50725: ['Exif.Image.ReductionMatrix1', 'SRational', 'ReductionMatrix1 defines a dimensionality reduction matrix for use as the first stage in converting color camera native space values to XYZ values, under the first calibration illuminant. This tag may only be used if ColorPlanes is greater than 3. The matrix is stored in row scan order.'],
    50726: ['Exif.Image.ReductionMatrix2', 'SRational', 'ReductionMatrix2 defines a dimensionality reduction matrix for use as the first stage in converting color camera native space values to XYZ values, under the second calibration illuminant. This tag may only be used if ColorPlanes is greater than 3. The matrix is stored in row scan order.'],
    50727: ['Exif.Image.AnalogBalance', 'Rational', 'Normally the stored raw values are not white balanced, since any digital white balancing will reduce the dynamic range of the final image if the user decides to later adjust the white balance; however, if camera hardware is capable of white balancing the color channels before the signal is digitized, it can improve the dynamic range of the final image. AnalogBalance defines the gain, either analog (recommended) or digital (not recommended) that has been applied the stored raw values.'],
    50728: ['Exif.Image.AsShotNeutral', 'Short', 'Specifies the selected white balance at time of capture, encoded as the coordinates of a perfectly neutral color in linear reference space values. The inclusion of this tag precludes the inclusion of the AsShotWhiteXY tag.'],
    50729: ['Exif.Image.AsShotWhiteXY', 'Rational', 'Specifies the selected white balance at time of capture, encoded as x-y chromaticity coordinates. The inclusion of this tag precludes the inclusion of the AsShotNeutral tag.'],
    50730: ['Exif.Image.BaselineExposure', 'SRational', 'Camera models vary in the trade-off they make between highlight headroom and shadow noise. Some leave a significant amount of highlight headroom during a normal exposure. This allows significant negative exposure compensation to be applied during raw conversion, but also means normal exposures will contain more shadow noise. Other models leave less headroom during normal exposures. This allows for less negative exposure compensation, but results in lower shadow noise for normal exposures. Because of these differences, a raw converter needs to vary the zero point of its exposure compensation control from model to model. BaselineExposure specifies by how much (in EV units) to move the zero point. Positive values result in brighter default results, while negative values result in darker default results.'],
    50731: ['Exif.Image.BaselineNoise', 'Rational', 'Specifies the relative noise level of the camera model at a baseline ISO value of 100, compared to a reference camera model. Since noise levels tend to vary approximately with the square root of the ISO value, a raw converter can use this value, combined with the current ISO, to estimate the relative noise level of the current image.'],
    50732: ['Exif.Image.BaselineSharpness', 'Rational', 'Specifies the relative amount of sharpening required for this camera model, compared to a reference camera model. Camera models vary in the strengths of their anti-aliasing filters. Cameras with weak or no filters require less sharpening than cameras with strong anti-aliasing filters.'],
    50733: ['Exif.Image.BayerGreenSplit', 'Long', 'Only applies to CFA images using a Bayer pattern filter array. This tag specifies, in arbitrary units, how closely the values of the green pixels in the blue/green rows track the values of the green pixels in the red/green rows. A value of zero means the two kinds of green pixels track closely, while a non-zero value means they sometimes diverge. The useful range for this tag is from 0 (no divergence) to about 5000 (quite large divergence).'],
    50734: ['Exif.Image.LinearResponseLimit', 'Rational', 'Some sensors have an unpredictable non-linearity in their response as they near the upper limit of their encoding range. This non-linearity results in color shifts in the highlight areas of the resulting image unless the raw converter compensates for this effect. LinearResponseLimit specifies the fraction of the encoding range above which the response may become significantly non-linear.'],
    50735: ['Exif.Image.CameraSerialNumber', 'Ascii', 'CameraSerialNumber contains the serial number of the camera or camera body that captured the image.'],
    50736: ['Exif.Image.LensInfo', 'Rational', 'Contains information about the lens that captured the image. If the minimum f-stops are unknown, they should be encoded as 0/0.'],
    50737: ['Exif.Image.ChromaBlurRadius', 'Rational', "ChromaBlurRadius provides a hint to the DNG reader about how much chroma blur should be applied to the image. If this tag is omitted, the reader will use its default amount of chroma blurring. Normally this tag is only included for non-CFA images, since the amount of chroma blur required for mosaic images is highly dependent on the de-mosaic algorithm, in which case the DNG reader's default value is likely optimized for its particular de-mosaic algorithm."],
    50738: ['Exif.Image.AntiAliasStrength', 'Rational', "Provides a hint to the DNG reader about how strong the camera's anti-alias filter is. A value of 0.0 means no anti-alias filter (i.e., the camera is prone to aliasing artifacts with some subjects), while a value of 1.0 means a strong anti-alias filter (i.e., the camera almost never has aliasing artifacts)."],
    50739: ['Exif.Image.ShadowScale', 'SRational', "This tag is used by Adobe Camera Raw to control the sensitivity of its 'Shadows' slider."],
    50740: ['Exif.Image.DNGPrivateData', 'Byte', 'Provides a way for camera manufacturers to store private data in the DNG file for use by their own raw converters, and to have that data preserved by programs that edit DNG files.'],
    50741: ['Exif.Image.MakerNoteSafety', 'Short', 'MakerNoteSafety lets the DNG reader know whether the EXIF MakerNote tag is safe to preserve along with the rest of the EXIF data. File browsers and other image management software processing an image with a preserved MakerNote should be aware that any thumbnail image embedded in the MakerNote may be stale, and may not reflect the current state of the full size image.'],
    50778: ['Exif.Image.CalibrationIlluminant1', 'Short', 'The illuminant used for the first set of color calibration tags (ColorMatrix1, CameraCalibration1, ReductionMatrix1). The legal values for this tag are the same as the legal values for the LightSource EXIF tag. If set to 255 (Other), then the IFD must also include a IlluminantData1 tag to specify the x-y chromaticity or spectral power distribution function for this illuminant.'],
    50779: ['Exif.Image.CalibrationIlluminant2', 'Short', 'The illuminant used for an optional second set of color calibration tags (ColorMatrix2, CameraCalibration2, ReductionMatrix2). The legal values for this tag are the same as the legal values for the CalibrationIlluminant1 tag; however, if both are included, neither is allowed to have a value of 0 (unknown). If set to 255 (Other), then the IFD must also include a IlluminantData2 tag to specify the x-y chromaticity or spectral power distribution function for this illuminant.'],
    50780: ['Exif.Image.BestQualityScale', 'Rational', 'For some cameras, the best possible image quality is not achieved by preserving the total pixel count during conversion. For example, Fujifilm SuperCCD images have maximum detail when their total pixel count is doubled. This tag specifies the amount by which the values of the DefaultScale tag need to be multiplied to achieve the best quality image size.'],
    50781: ['Exif.Image.RawDataUniqueID', 'Byte', "This tag contains a 16-byte unique identifier for the raw image data in the DNG file. DNG readers can use this tag to recognize a particular raw image, even if the file's name or the metadata contained in the file has been changed. If a DNG writer creates such an identifier, it should do so using an algorithm that will ensure that it is very unlikely two different images will end up having the same identifier."],
    50827: ['Exif.Image.OriginalRawFileName', 'Byte', 'If the DNG file was converted from a non-DNG raw file, then this tag contains the file name of that original raw file.'],
    50828: ['Exif.Image.OriginalRawFileData', 'Undefined', 'If the DNG file was converted from a non-DNG raw file, then this tag contains the compressed contents of that original raw file. The contents of this tag always use the big-endian byte order. The tag contains a sequence of data blocks. Future versions of the DNG specification may define additional data blocks, so DNG readers should ignore extra bytes when parsing this tag. DNG readers should also detect the case where data blocks are missing from the end of the sequence, and should assume a default value for all the missing blocks. There are no padding or alignment bytes between data blocks.'],
    50829: ['Exif.Image.ActiveArea', 'Long', 'This rectangle defines the active (non-masked) pixels of the sensor. The order of the rectangle coordinates is: top, left, bottom, right.'],
    50830: ['Exif.Image.MaskedAreas', 'Long', "This tag contains a list of non-overlapping rectangle coordinates of fully masked pixels, which can be optionally used by DNG readers to measure the black encoding level. The order of each rectangle's coordinates is: top, left, bottom, right. If the raw image data has already had its black encoding level subtracted, then this tag should not be used, since the masked pixels are no longer useful."],
    50831: ['Exif.Image.AsShotICCProfile', 'Undefined', 'This tag contains an ICC profile that, in conjunction with the AsShotPreProfileMatrix tag, provides the camera manufacturer with a way to specify a default color rendering from camera color space coordinates (linear reference values) into the ICC profile connection space. The ICC profile connection space is an output referred colorimetric space, whereas the other color calibration tags in DNG specify a conversion into a scene referred colorimetric space. This means that the rendering in this profile should include any desired tone and gamut mapping needed to convert between scene referred values and output referred values.'],
    50832: ['Exif.Image.AsShotPreProfileMatrix', 'SRational', 'This tag is used in conjunction with the AsShotICCProfile tag. It specifies a matrix that should be applied to the camera color space coordinates before processing the values through the ICC profile specified in the AsShotICCProfile tag. The matrix is stored in the row scan order. If ColorPlanes is greater than three, then this matrix can (but is not required to) reduce the dimensionality of the color data down to three components, in which case the AsShotICCProfile should have three rather than ColorPlanes input components.'],
    50833: ['Exif.Image.CurrentICCProfile', 'Undefined', 'This tag is used in conjunction with the CurrentPreProfileMatrix tag. The CurrentICCProfile and CurrentPreProfileMatrix tags have the same purpose and usage as the AsShotICCProfile and AsShotPreProfileMatrix tag pair, except they are for use by raw file editors rather than camera manufacturers.'],
    50834: ['Exif.Image.CurrentPreProfileMatrix', 'SRational', 'This tag is used in conjunction with the CurrentICCProfile tag. The CurrentICCProfile and CurrentPreProfileMatrix tags have the same purpose and usage as the AsShotICCProfile and AsShotPreProfileMatrix tag pair, except they are for use by raw file editors rather than camera manufacturers.'],
    50879: ['Exif.Image.ColorimetricReference', 'Short', 'The DNG color model documents a transform between camera colors and CIE XYZ values. This tag describes the colorimetric reference for the CIE XYZ values. 0 = The XYZ values are scene-referred. 1 = The XYZ values are output-referred, using the ICC profile perceptual dynamic range. This tag allows output-referred data to be stored in DNG files and still processed correctly by DNG readers.'],
    50931: ['Exif.Image.CameraCalibrationSignature', 'Byte', 'A UTF-8 encoded string associated with the CameraCalibration1 and CameraCalibration2 tags. The CameraCalibration1 and CameraCalibration2 tags should only be used in the DNG color transform if the string stored in the CameraCalibrationSignature tag exactly matches the string stored in the ProfileCalibrationSignature tag for the selected camera profile.'],
    50932: ['Exif.Image.ProfileCalibrationSignature', 'Byte', 'A UTF-8 encoded string associated with the camera profile tags. The CameraCalibration1 and CameraCalibration2 tags should only be used in the DNG color transfer if the string stored in the CameraCalibrationSignature tag exactly matches the string stored in the ProfileCalibrationSignature tag for the selected camera profile.'],
    50933: ['Exif.Image.ExtraCameraProfiles', 'Long', 'A list of file offsets to extra Camera Profile IFDs. Note that the primary camera profile tags should be stored in IFD 0, and the ExtraCameraProfiles tag should only be used if there is more than one camera profile stored in the DNG file.'],
    50934: ['Exif.Image.AsShotProfileName', 'Byte', 'A UTF-8 encoded string containing the name of the "as shot" camera profile, if any.'],
    50935: ['Exif.Image.NoiseReductionApplied', 'Rational', 'This tag indicates how much noise reduction has been applied to the raw data on a scale of 0.0 to 1.0. A 0.0 value indicates that no noise reduction has been applied. A 1.0 value indicates that the "ideal" amount of noise reduction has been applied, i.e. that the DNG reader should not apply additional noise reduction by default. A value of 0/0 indicates that this parameter is unknown.'],
    50936: ['Exif.Image.ProfileName', 'Byte', 'A UTF-8 encoded string containing the name of the camera profile. This tag is optional if there is only a single camera profile stored in the file but is required for all camera profiles if there is more than one camera profile stored in the file.'],
    50937: ['Exif.Image.ProfileHueSatMapDims', 'Long', 'This tag specifies the number of input samples in each dimension of the hue/saturation/value mapping tables. The data for these tables are stored in ProfileHueSatMapData1, ProfileHueSatMapData2 and ProfileHueSatMapData3 tags. The most common case has ValueDivisions equal to 1, so only hue and saturation are used as inputs to the mapping table.'],
    50938: ['Exif.Image.ProfileHueSatMapData1', 'Float', 'This tag contains the data for the first hue/saturation/value mapping table. Each entry of the table contains three 32-bit IEEE floating-point values. The first entry is hue shift in degrees; the second entry is saturation scale factor; and the third entry is a value scale factor. The table entries are stored in the tag in nested loop order, with the value divisions in the outer loop, the hue divisions in the middle loop, and the saturation divisions in the inner loop. All zero input saturation entries are required to have a value scale factor of 1.0.'],
    50939: ['Exif.Image.ProfileHueSatMapData2', 'Float', 'This tag contains the data for the second hue/saturation/value mapping table. Each entry of the table contains three 32-bit IEEE floating-point values. The first entry is hue shift in degrees; the second entry is a saturation scale factor; and the third entry is a value scale factor. The table entries are stored in the tag in nested loop order, with the value divisions in the outer loop, the hue divisions in the middle loop, and the saturation divisions in the inner loop. All zero input saturation entries are required to have a value scale factor of 1.0.'],
    50940: ['Exif.Image.ProfileToneCurve', 'Float', 'This tag contains a default tone curve that can be applied while processing the image as a starting point for user adjustments. The curve is specified as a list of 32-bit IEEE floating-point value pairs in linear gamma. Each sample has an input value in the range of 0.0 to 1.0, and an output value in the range of 0.0 to 1.0. The first sample is required to be (0.0, 0.0), and the last sample is required to be (1.0, 1.0). Interpolated the curve using a cubic spline.'],
    50941: ['Exif.Image.ProfileEmbedPolicy', 'Long', 'This tag contains information about the usage rules for the associated camera profile.'],
    50942: ['Exif.Image.ProfileCopyright', 'Byte', 'A UTF-8 encoded string containing the copyright information for the camera profile. This string always should be preserved along with the other camera profile tags.'],
    50964: ['Exif.Image.ForwardMatrix1', 'SRational', 'This tag defines a matrix that maps white balanced camera colors to XYZ D50 colors.'],
    50965: ['Exif.Image.ForwardMatrix2', 'SRational', 'This tag defines a matrix that maps white balanced camera colors to XYZ D50 colors.'],
    50966: ['Exif.Image.PreviewApplicationName', 'Byte', 'A UTF-8 encoded string containing the name of the application that created the preview stored in the IFD.'],
    50967: ['Exif.Image.PreviewApplicationVersion', 'Byte', 'A UTF-8 encoded string containing the version number of the application that created the preview stored in the IFD.'],
    50968: ['Exif.Image.PreviewSettingsName', 'Byte', 'A UTF-8 encoded string containing the name of the conversion settings (for example, snapshot name) used for the preview stored in the IFD.'],
    50969: ['Exif.Image.PreviewSettingsDigest', 'Byte', 'A unique ID of the conversion settings (for example, MD5 digest) used to render the preview stored in the IFD.'],
    50970: ['Exif.Image.PreviewColorSpace', 'Long', 'This tag specifies the color space in which the rendered preview in this IFD is stored. The default value for this tag is sRGB for color previews and Gray Gamma 2.2 for monochrome previews.'],
    50971: ['Exif.Image.PreviewDateTime', 'Ascii', 'This tag is an ASCII string containing the name of the date/time at which the preview stored in the IFD was rendered. The date/time is encoded using ISO 8601 format.'],
    50972: ['Exif.Image.RawImageDigest', 'Undefined', 'This tag is an MD5 digest of the raw image data. All pixels in the image are processed in row-scan order. Each pixel is zero padded to 16 or 32 bits deep (16-bit for data less than or equal to 16 bits deep, 32-bit otherwise). The data for each pixel is processed in little-endian byte order.'],
    50973: ['Exif.Image.OriginalRawFileDigest', 'Undefined', 'This tag is an MD5 digest of the data stored in the OriginalRawFileData tag.'],
    50974: ['Exif.Image.SubTileBlockSize', 'Long', 'Normally, the pixels within a tile are stored in simple row-scan order. This tag specifies that the pixels within a tile should be grouped first into rectangular blocks of the specified size. These blocks are stored in row-scan order. Within each block, the pixels are stored in row-scan order. The use of a non-default value for this tag requires setting the DNGBackwardVersion tag to at least 1.2.0.0.'],
    50975: ['Exif.Image.RowInterleaveFactor', 'Long', 'This tag specifies that rows of the image are stored in interleaved order. The value of the tag specifies the number of interleaved fields. The use of a non-default value for this tag requires setting the DNGBackwardVersion tag to at least 1.2.0.0.'],
    50981: ['Exif.Image.ProfileLookTableDims', 'Long', 'This tag specifies the number of input samples in each dimension of a default "look" table. The data for this table is stored in the ProfileLookTableData tag.'],
    50982: ['Exif.Image.ProfileLookTableData', 'Float', 'This tag contains a default "look" table that can be applied while processing the image as a starting point for user adjustment. This table uses the same format as the tables stored in the ProfileHueSatMapData1 and ProfileHueSatMapData2 tags, and is applied in the same color space. However, it should be applied later in the processing pipe, after any exposure compensation and/or fill light stages, but before any tone curve stage. Each entry of the table contains three 32-bit IEEE floating-point values. The first entry is hue shift in degrees, the second entry is a saturation scale factor, and the third entry is a value scale factor. The table entries are stored in the tag in nested loop order, with the value divisions in the outer loop, the hue divisions in the middle loop, and the saturation divisions in the inner loop. All zero input saturation entries are required to have a value scale factor of 1.0.'],
    51008: ['Exif.Image.OpcodeList1', 'Undefined', 'Specifies the list of opcodes that should be applied to the raw image, as read directly from the file.'],
    51009: ['Exif.Image.OpcodeList2', 'Undefined', 'Specifies the list of opcodes that should be applied to the raw image, just after it has been mapped to linear reference values.'],
    51022: ['Exif.Image.OpcodeList3', 'Undefined', 'Specifies the list of opcodes that should be applied to the raw image, just after it has been demosaiced.'],
    51041: ['Exif.Image.NoiseProfile', 'Double', 'NoiseProfile describes the amount of noise in a raw image. Specifically, this tag models the amount of signal-dependent photon (shot) noise and signal-independent sensor readout noise, two common sources of noise in raw images. The model assumes that the noise is white and spatially independent, ignoring fixed pattern effects and other sources of noise (e.g., pixel response non-uniformity, spatially-dependent thermal effects, etc.).'],
    51043: ['Exif.Image.TimeCodes', 'Byte', 'The optional TimeCodes tag shall contain an ordered array of time codes. All time codes shall be 8 bytes long and in binary format. The tag may contain from 1 to 10 time codes. When the tag contains more than one time code, the first one shall be the default time code. This specification does not prescribe how to use multiple time codes. Each time code shall be as defined for the 8-byte time code structure in SMPTE 331M-2004, Section 8.3. See also SMPTE 12-1-2008 and SMPTE 309-1999.'],
    51044: ['Exif.Image.FrameRate', 'SRational', 'The optional FrameRate tag shall specify the video frame rate in number of image frames per second, expressed as a signed rational number. The numerator shall be non-negative and the denominator shall be positive. This field value is identical to the sample rate field in SMPTE 377-1-2009.'],
    51058: ['Exif.Image.TStop', 'SRational', 'The optional TStop tag shall specify the T-stop of the actual lens, expressed as an unsigned rational number. T-stop is also known as T-number or the photometric aperture of the lens. (F-number is the geometric aperture of the lens.) When the exact value is known, the T-stop shall be specified using a single number. Alternately, two numbers shall be used to indicate a T-stop range, in which case the first number shall be the minimum T-stop and the second number shall be the maximum T-stop.'],
    51081: ['Exif.Image.ReelName', 'Ascii', 'The optional ReelName tag shall specify a name for a sequence of images, where each image in the sequence has a unique image identifier (including but not limited to file name, frame number, date time, time code).'],
    51105: ['Exif.Image.CameraLabel', 'Ascii', 'The optional CameraLabel tag shall specify a text label for how the camera is used or assigned in this clip. This tag is similar to CameraLabel in XMP.'],
    51089: ['Exif.Image.OriginalDefaultFinalSize', 'Long', 'If this file is a proxy for a larger original DNG file, this tag specifics the default final size of the larger original file from which this proxy was generated. The default value for this tag is default final size of the current DNG file, which is DefaultCropSize * DefaultScale.'],
    51090: ['Exif.Image.OriginalBestQualityFinalSize', 'Long', 'If this file is a proxy for a larger original DNG file, this tag specifics the best quality final size of the larger original file from which this proxy was generated. The default value for this tag is the OriginalDefaultFinalSize, if specified. Otherwise the default value for this tag is the best quality size of the current DNG file, which is DefaultCropSize * DefaultScale * BestQualityScale.'],
    51091: ['Exif.Image.OriginalDefaultCropSize', 'Long', 'If this file is a proxy for a larger original DNG file, this tag specifics the DefaultCropSize of the larger original file from which this proxy was generated. The default value for this tag is OriginalDefaultFinalSize, if specified. Otherwise, the default value for this tag is the DefaultCropSize of the current DNG file.'],
    51107: ['Exif.Image.ProfileHueSatMapEncoding', 'Long', 'Provides a way for color profiles to specify how indexing into a 3D HueSatMap is performed during raw conversion. This tag is not applicable to 2.5D HueSatMap tables (i.e., where the Value dimension is 1).'],
    51108: ['Exif.Image.ProfileLookTableEncoding', 'Long', 'Provides a way for color profiles to specify how indexing into a 3D LookTable is performed during raw conversion. This tag is not applicable to a 2.5D LookTable (i.e., where the Value dimension is 1).'],
    51109: ['Exif.Image.BaselineExposureOffset', 'SRational', 'Provides a way for color profiles to increase or decrease exposure during raw conversion. BaselineExposureOffset specifies the amount (in EV units) to add to the BaselineExposure tag during image rendering. For example, if the BaselineExposure value for a given camera model is +0.3, and the BaselineExposureOffset value for a given camera profile used to render an image for that camera model is -0.7, then the actual default exposure value used during rendering will be +0.3 - 0.7 = -0.4.'],
    51110: ['Exif.Image.DefaultBlackRender', 'Long', 'This optional tag in a color profile provides a hint to the raw converter regarding how to handle the black point (e.g., flare subtraction) during rendering. If set to Auto, the raw converter should perform black subtraction during rendering. If set to None, the raw converter should not perform any black subtraction during rendering.'],
    51111: ['Exif.Image.NewRawImageDigest', 'Byte', 'This tag is a modified MD5 digest of the raw image data. It has been updated from the algorithm used to compute the RawImageDigest tag be more multi-processor friendly, and to support lossy compression algorithms.'],
    51112: ['Exif.Image.RawToPreviewGain', 'Double', 'The gain (what number the sample values are multiplied by) between the main raw IFD and the preview IFD containing this tag.'],
    51125: ['Exif.Image.DefaultUserCrop', 'Rational', 'Specifies a default user crop rectangle in relative coordinates. The values must satisfy: 0.0 <= top < bottom <= 1.0, 0.0 <= left < right <= 1.0.The default values of (top = 0, left = 0, bottom = 1, right = 1) correspond exactly to the default crop rectangle (as specified by the DefaultCropOrigin and DefaultCropSize tags).'],
    51177: ['Exif.Image.DepthFormat', 'Short', 'Specifies the encoding of any depth data in the file. Can be unknown (apart from nearer distances being closer to zero, and farther distances being closer to the maximum value), linear (values vary linearly from zero representing DepthNear to the maximum value representing DepthFar), or inverse (values are stored inverse linearly, with zero representing DepthNear and the maximum value representing DepthFar).'],
    51178: ['Exif.Image.DepthNear', 'Rational', 'Specifies distance from the camera represented by the zero value in the depth map. 0/0 means unknown.'],
    51179: ['Exif.Image.DepthFar', 'Rational', 'Specifies distance from the camera represented by the maximum value in the depth map. 0/0 means unknown. 1/0 means infinity, which is valid for unknown and inverse depth formats.'],
    51180: ['Exif.Image.DepthUnits', 'Short', 'Specifies the measurement units for the DepthNear and DepthFar tags.'],
    51181: ['Exif.Image.DepthMeasureType', 'Short', 'Specifies the measurement geometry for the depth map. Can be unknown, measured along the optical axis, or measured along the optical ray passing through each pixel.'],
    51182: ['Exif.Image.EnhanceParams', 'Ascii', 'A string that documents how the enhanced image data was processed.'],
    52525: ['Exif.Image.ProfileGainTableMap', 'Undefined', 'Contains spatially varying gain tables that can be applied while processing the image as a starting point for user adjustments.'],
    52526: ['Exif.Image.SemanticName', 'Ascii', 'A string that identifies the semantic mask.'],
    52528: ['Exif.Image.SemanticInstanceID', 'Ascii', 'A string that identifies a specific instance in a semantic mask.'],
    52529: ['Exif.Image.CalibrationIlluminant3', 'Short', 'The illuminant used for an optional third set of color calibration tags (ColorMatrix3, CameraCalibration3, ReductionMatrix3). The legal values for this tag are the same as the legal values for the LightSource EXIF tag; CalibrationIlluminant1 and CalibrationIlluminant2 must also be present. If set to 255 (Other), then the IFD must also include a IlluminantData3 tag to specify the x-y chromaticity or spectral power distribution function for this illuminant.'],
    52530: ['Exif.Image.CameraCalibration3', 'SRational', 'CameraCalibration3 defines a calibration matrix that transforms reference camera native space values to individual camera native space values under the third calibration illuminant. The matrix is stored in row scan order. This matrix is stored separately from the matrix specified by the ColorMatrix3 tag to allow raw converters to swap in replacement color matrices based on UniqueCameraModel tag, while still taking advantage of any per-individual camera calibration performed by the camera manufacturer.'],
    52531: ['Exif.Image.ColorMatrix3', 'SRational', 'ColorMatrix3 defines a transformation matrix that converts XYZ values to reference camera native color space values, under the third calibration illuminant. The matrix values are stored in row scan order.'],
    52532: ['Exif.Image.ForwardMatrix3', 'SRational', 'This tag defines a matrix that maps white balanced camera colors to XYZ D50 colors.'],
    52533: ['Exif.Image.IlluminantData1', 'Undefined', 'When the CalibrationIlluminant1 tag is set to 255 (Other), then the IlluminantData1 tag is required and specifies the data for the first illuminant. Otherwise, this tag is ignored. The illuminant data may be specified as either a x-y chromaticity coordinate or as a spectral power distribution function.'],
    52534: ['Exif.Image.IlluminantData2', 'Undefined', 'When the CalibrationIlluminant2 tag is set to 255 (Other), then the IlluminantData2 tag is required and specifies the data for the second illuminant. Otherwise, this tag is ignored. The format of the data is the same as IlluminantData1.'],
    52535: ['Exif.Image.IlluminantData3', 'Undefined', 'When the CalibrationIlluminant3 tag is set to 255 (Other), then the IlluminantData3 tag is required and specifies the data for the third illuminant. Otherwise, this tag is ignored. The format of the data is the same as IlluminantData1.'],
    52536: ['Exif.Image.MaskSubArea', 'Long', "This tag identifies the crop rectangle of this IFD's mask, relative to the main image."],
    52537: ['Exif.Image.ProfileHueSatMapData3', 'Float', 'This tag contains the data for the third hue/saturation/value mapping table. Each entry of the table contains three 32-bit IEEE floating-point values. The first entry is hue shift in degrees; the second entry is saturation scale factor; and the third entry is a value scale factor. The table entries are stored in the tag in nested loop order, with the value divisions in the outer loop, the hue divisions in the middle loop, and the saturation divisions in the inner loop. All zero input saturation entries are required to have a value scale factor of 1.0.'],
    52538: ['Exif.Image.ReductionMatrix3', 'SRational', 'ReductionMatrix3 defines a dimensionality reduction matrix for use as the first stage in converting color camera native space values to XYZ values, under the third calibration illuminant. This tag may only be used if ColorPlanes is greater than 3. The matrix is stored in row scan order.'],
    52543: ['Exif.Image.RGBTables', 'Undefined', 'This tag specifies color transforms that can be applied to masked image regions. Color transforms are specified using RGB-to-RGB color lookup tables. These tables are associated with Semantic Masks to limit the color transform to a sub-region of the image. The overall color transform is a linear combination of the color tables, weighted by their corresponding Semantic Masks.'],
    52544: ['Exif.Image.ProfileGainTableMap2', 'Undefined', 'This tag is an extended version of ProfileGainTableMap.'],
    52547: ['Exif.Image.ColumnInterleaveFactor', 'Long', 'This tag specifies that columns of the image are stored in interleaved order. The value of the tag specifies the number of interleaved fields. The use of a non-default value for this tag requires setting the DNGBackwardVersion tag to at least 1.7.1.0.'],
    52548: ['Exif.Image.ImageSequenceInfo', 'Undefined', 'This is an informative tag that describes how the image file relates to other image files captured in a sequence. Applications include focus stacking, merging multiple frames to reduce noise, time lapses, exposure brackets, stitched images for super resolution, and so on.'],
    52550: ['Exif.Image.ImageStats', 'Undefined', 'This is an informative tag that provides basic statistical information about the pixel values of the image in this IFD. Possible applications include normalizing brightness of images when multiple images are displayed together (especially when mixing Standard Dynamic Range and High Dynamic Range images), identifying underexposed or overexposed images, and so on.'],
    52551: ['Exif.Image.ProfileDynamicRange', 'Undefined', 'This tag describes the intended rendering output dynamic range for a given camera profile.'],
    52552: ['Exif.Image.ProfileGroupName', 'Ascii', "A UTF-8 encoded string containing the 'group name' of the camera profile. The purpose of this tag is to associate two or more related camera profiles into a common group."],
    52553: ['Exif.Image.JXLDistance', 'Float', 'This optional tag specifies the distance parameter used to encode the JPEG XL data in this IFD. A value of 0.0 means lossless compression, while values greater than 0.0 means lossy compression.'],
    52554: ['Exif.Image.JXLEffort', 'Long', 'This optional tag specifies the effort parameter used to encode the JPEG XL data in this IFD. Values range from 1 (low) to 9 (high).'],
    52555: ['Exif.Image.JXLDecodeSpeed', 'Long', 'This optional tag specifies the decode speed parameter used to encode the JPEG XL data in this IFD. Values range from 1 (slow) to 4 (fast).'],
    33434: ['Exif.Photo.ExposureTime', 'Rational', 'Exposure time, given in seconds (sec).'],
    33437: ['Exif.Photo.FNumber', 'Rational', 'The F number.'],
    34850: ['Exif.Photo.ExposureProgram', 'Short', 'The class of the program used by the camera to set exposure when the picture is taken.'],
    34852: ['Exif.Photo.SpectralSensitivity', 'Ascii', 'Indicates the spectral sensitivity of each channel of the camera used. The tag value is an ASCII string compatible with the standard developed by the ASTM Technical Committee.'],
    34855: ['Exif.Photo.ISOSpeedRatings', 'Short', 'Indicates the ISO Speed and ISO Latitude of the camera or input device as specified in ISO 12232.'],
    34856: ['Exif.Photo.OECF', 'Undefined', 'Indicates the Opto-Electoric Conversion Function (OECF) specified in ISO 14524. <OECF> is the relationship between the camera optical input and the image values.'],
    34864: ['Exif.Photo.SensitivityType', 'Short', 'The SensitivityType tag indicates which one of the parameters of ISO12232 is the PhotographicSensitivity tag. Although it is an optional tag, it should be recorded when a PhotographicSensitivity tag is recorded. Value = 4, 5, 6, or 7 may be used in case that the values of plural parameters are the same.'],
    34865: ['Exif.Photo.StandardOutputSensitivity', 'Long', 'This tag indicates the standard output sensitivity value of a camera or input device defined in ISO 12232. When recording this tag, the PhotographicSensitivity and SensitivityType tags shall also be recorded.'],
    34866: ['Exif.Photo.RecommendedExposureIndex', 'Long', 'This tag indicates the recommended exposure index value of a camera or input device defined in ISO 12232. When recording this tag, the PhotographicSensitivity and SensitivityType tags shall also be recorded.'],
    34867: ['Exif.Photo.ISOSpeed', 'Long', 'This tag indicates the ISO speed value of a camera or input device that is defined in ISO 12232. When recording this tag, the PhotographicSensitivity and SensitivityType tags shall also be recorded.'],
    34868: ['Exif.Photo.ISOSpeedLatitudeyyy', 'Long', 'This tag indicates the ISO speed latitude yyy value of a camera or input device that is defined in ISO 12232. However, this tag shall not be recorded without ISOSpeed and ISOSpeedLatitudezzz.'],
    34869: ['Exif.Photo.ISOSpeedLatitudezzz', 'Long', 'This tag indicates the ISO speed latitude zzz value of a camera or input device that is defined in ISO 12232. However, this tag shall not be recorded without ISOSpeed and ISOSpeedLatitudeyyy.'],
    36864: ['Exif.Photo.ExifVersion', 'Undefined', 'The version of this standard supported. Nonexistence of this field is taken to mean nonconformance to the standard.'],
    36867: ['Exif.Photo.DateTimeOriginal', 'Ascii', 'The date and time when the original image data was generated. For a digital still camera the date and time the picture was taken are recorded.'],
    36868: ['Exif.Photo.DateTimeDigitized', 'Ascii', 'The date and time when the image was stored as digital data.'],
    36880: ['Exif.Photo.OffsetTime', 'Ascii', 'Time difference from Universal Time Coordinated including daylight saving time of DateTime tag.'],
    36881: ['Exif.Photo.OffsetTimeOriginal', 'Ascii', 'Time difference from Universal Time Coordinated including daylight saving time of DateTimeOriginal tag.'],
    36882: ['Exif.Photo.OffsetTimeDigitized', 'Ascii', 'Time difference from Universal Time Coordinated including daylight saving time of DateTimeDigitized tag.'],
    37121: ['Exif.Photo.ComponentsConfiguration', 'Undefined', 'Information specific to compressed data. The channels of each component are arranged in order from the 1st component to the 4th. For uncompressed data the data arrangement is given in the <PhotometricInterpretation> tag. However, since <PhotometricInterpretation> can only express the order of Y, Cb and Cr, this tag is provided for cases when compressed data uses components other than Y, Cb, and Cr and to enable support of other sequences.'],
    37122: ['Exif.Photo.CompressedBitsPerPixel', 'Rational', 'Information specific to compressed data. The compression mode used for a compressed image is indicated in unit bits per pixel.'],
    37377: ['Exif.Photo.ShutterSpeedValue', 'SRational', 'Shutter speed. The unit is the APEX (Additive System of Photographic Exposure) setting.'],
    37378: ['Exif.Photo.ApertureValue', 'Rational', 'The lens aperture. The unit is the APEX value.'],
    37379: ['Exif.Photo.BrightnessValue', 'SRational', 'The value of brightness. The unit is the APEX value. Ordinarily it is given in the range of -99.99 to 99.99.'],
    37380: ['Exif.Photo.ExposureBiasValue', 'SRational', 'The exposure bias. The units is the APEX value. Ordinarily it is given in the range of -99.99 to 99.99.'],
    37381: ['Exif.Photo.MaxApertureValue', 'Rational', 'The smallest F number of the lens. The unit is the APEX value. Ordinarily it is given in the range of 00.00 to 99.99, but it is not limited to this range.'],
    37382: ['Exif.Photo.SubjectDistance', 'Rational', 'The distance to the subject, given in meters.'],
    37383: ['Exif.Photo.MeteringMode', 'Short', 'The metering mode.'],
    37384: ['Exif.Photo.LightSource', 'Short', 'The kind of light source.'],
    37385: ['Exif.Photo.Flash', 'Short', 'This tag is recorded when an image is taken using a strobe light (flash).'],
    37386: ['Exif.Photo.FocalLength', 'Rational', 'The actual focal length of the lens, in mm. Conversion is not made to the focal length of a 35 mm film camera.'],
    37396: ['Exif.Photo.SubjectArea', 'Short', 'This tag indicates the location and area of the main subject in the overall scene.'],
    37500: ['Exif.Photo.MakerNote', 'Undefined', 'A tag for manufacturers of Exif writers to record any desired information. The contents are up to the manufacturer.'],
    37510: ['Exif.Photo.UserComment', 'Comment', 'A tag for Exif users to write keywords or comments on the image besides those in <ImageDescription>, and without the character code limitations of the <ImageDescription> tag.'],
    37520: ['Exif.Photo.SubSecTime', 'Ascii', 'A tag used to record fractions of seconds for the <DateTime> tag.'],
    37521: ['Exif.Photo.SubSecTimeOriginal', 'Ascii', 'A tag used to record fractions of seconds for the <DateTimeOriginal> tag.'],
    37522: ['Exif.Photo.SubSecTimeDigitized', 'Ascii', 'A tag used to record fractions of seconds for the <DateTimeDigitized> tag.'],
    37888: ['Exif.Photo.Temperature', 'SRational', 'Temperature as the ambient situation at the shot, for example the room temperature where the photographer was holding the camera. The unit is degrees C.'],
    37889: ['Exif.Photo.Humidity', 'Rational', 'Humidity as the ambient situation at the shot, for example the room humidity where the photographer was holding the camera. The unit is %.'],
    37890: ['Exif.Photo.Pressure', 'Rational', 'Pressure as the ambient situation at the shot, for example the room atmosphere where the photographer was holding the camera or the water pressure under the sea. The unit is hPa.'],
    37891: ['Exif.Photo.WaterDepth', 'SRational', 'Water depth as the ambient situation at the shot, for example the water depth of the camera at underwater photography. The unit is m.'],
    37892: ['Exif.Photo.Acceleration', 'Rational', 'Acceleration (a scalar regardless of direction) as the ambient situation at the shot, for example the driving acceleration of the vehicle which the photographer rode on at the shot. The unit is mGal (10e-5 m/s^2).'],
    37893: ['Exif.Photo.CameraElevationAngle', 'SRational', 'Elevation/depression. angle of the orientation of the camera(imaging optical axis) as the ambient situation at the shot. The unit is degrees.'],
    40960: ['Exif.Photo.FlashpixVersion', 'Undefined', 'The FlashPix format version supported by a FPXR file.'],
    40961: ['Exif.Photo.ColorSpace', 'Short', 'The color space information tag is always recorded as the color space specifier. Normally sRGB is used to define the color space based on the PC monitor conditions and environment. If a color space other than sRGB is used, Uncalibrated is set. Image data recorded as Uncalibrated can be treated as sRGB when it is converted to FlashPix.'],
    40962: ['Exif.Photo.PixelXDimension', 'Long', 'Information specific to compressed data. When a compressed file is recorded, the valid width of the meaningful image must be recorded in this tag, whether or not there is padding data or a restart marker. This tag should not exist in an uncompressed file.'],
    40963: ['Exif.Photo.PixelYDimension', 'Long', 'Information specific to compressed data. When a compressed file is recorded, the valid height of the meaningful image must be recorded in this tag, whether or not there is padding data or a restart marker. This tag should not exist in an uncompressed file. Since data padding is unnecessary in the vertical direction, the number of lines recorded in this valid image height tag will in fact be the same as that recorded in the SOF.'],
    40964: ['Exif.Photo.RelatedSoundFile', 'Ascii', "This tag is used to record the name of an audio file related to the image data. The only relational information recorded here is the Exif audio file name and extension (an ASCII string consisting of 8 characters + '.' + 3 characters). The path is not recorded."],
    40965: ['Exif.Photo.InteroperabilityTag', 'Long', 'Interoperability IFD is composed of tags which stores the information to ensure the Interoperability and pointed by the following tag located in Exif IFD. The Interoperability structure of Interoperability IFD is the same as TIFF defined IFD structure but does not contain the image data characteristically compared with normal TIFF IFD.'],
    41483: ['Exif.Photo.FlashEnergy', 'Rational', 'Indicates the strobe energy at the time the image is captured, as measured in Beam Candle Power Seconds (BCPS).'],
    41484: ['Exif.Photo.SpatialFrequencyResponse', 'Undefined', 'This tag records the camera or input device spatial frequency table and SFR values in the direction of image width, image height, and diagonal direction, as specified in ISO 12233.'],
    41486: ['Exif.Photo.FocalPlaneXResolution', 'Rational', 'Indicates the number of pixels in the image width (X) direction per <FocalPlaneResolutionUnit> on the camera focal plane.'],
    41487: ['Exif.Photo.FocalPlaneYResolution', 'Rational', 'Indicates the number of pixels in the image height (V) direction per <FocalPlaneResolutionUnit> on the camera focal plane.'],
    41488: ['Exif.Photo.FocalPlaneResolutionUnit', 'Short', 'Indicates the unit for measuring <FocalPlaneXResolution> and <FocalPlaneYResolution>. This value is the same as the <ResolutionUnit>.'],
    41492: ['Exif.Photo.SubjectLocation', 'Short', 'Indicates the location of the main subject in the scene. The value of this tag represents the pixel at the center of the main subject relative to the left edge, prior to rotation processing as per the <Rotation> tag. The first value indicates the X column number and second indicates the Y row number.'],
    41493: ['Exif.Photo.ExposureIndex', 'Rational', 'Indicates the exposure index selected on the camera or input device at the time the image is captured.'],
    41495: ['Exif.Photo.SensingMethod', 'Short', 'Indicates the image sensor type on the camera or input device.'],
    41728: ['Exif.Photo.FileSource', 'Undefined', 'Indicates the image source. If a DSC recorded the image, this tag value of this tag always be set to 3, indicating that the image was recorded on a DSC.'],
    41729: ['Exif.Photo.SceneType', 'Undefined', 'Indicates the type of scene. If a DSC recorded the image, this tag value must always be set to 1, indicating that the image was directly photographed.'],
    41730: ['Exif.Photo.CFAPattern', 'Undefined', 'Indicates the color filter array (CFA) geometric pattern of the image sensor when a one-chip color area sensor is used. It does not apply to all sensing methods.'],
    41985: ['Exif.Photo.CustomRendered', 'Short', 'This tag indicates the use of special processing on image data, such as rendering geared to output. When special processing is performed, the reader is expected to disable or minimize any further processing.'],
    41986: ['Exif.Photo.ExposureMode', 'Short', 'This tag indicates the exposure mode set when the image was shot. In auto-bracketing mode, the camera shoots a series of frames of the same scene at different exposure settings.'],
    41987: ['Exif.Photo.WhiteBalance', 'Short', 'This tag indicates the white balance mode set when the image was shot.'],
    41988: ['Exif.Photo.DigitalZoomRatio', 'Rational', 'This tag indicates the digital zoom ratio when the image was shot. If the numerator of the recorded value is 0, this indicates that digital zoom was not used.'],
    41989: ['Exif.Photo.FocalLengthIn35mmFilm', 'Short', 'This tag indicates the equivalent focal length assuming a 35mm film camera, in mm. A value of 0 means the focal length is unknown. Note that this tag differs from the <FocalLength> tag.'],
    41990: ['Exif.Photo.SceneCaptureType', 'Short', 'This tag indicates the type of scene that was shot. It can also be used to record the mode in which the image was shot. Note that this differs from the <SceneType> tag.'],
    41991: ['Exif.Photo.GainControl', 'Short', 'This tag indicates the degree of overall image gain adjustment.'],
    41992: ['Exif.Photo.Contrast', 'Short', 'This tag indicates the direction of contrast processing applied by the camera when the image was shot.'],
    41993: ['Exif.Photo.Saturation', 'Short', 'This tag indicates the direction of saturation processing applied by the camera when the image was shot.'],
    41994: ['Exif.Photo.Sharpness', 'Short', 'This tag indicates the direction of sharpness processing applied by the camera when the image was shot.'],
    41995: ['Exif.Photo.DeviceSettingDescription', 'Undefined', 'This tag indicates information on the picture-taking conditions of a particular camera model. The tag is used only to indicate the picture-taking conditions in the reader.'],
    41996: ['Exif.Photo.SubjectDistanceRange', 'Short', 'This tag indicates the distance to the subject.'],
    42016: ['Exif.Photo.ImageUniqueID', 'Ascii', 'This tag indicates an identifier assigned uniquely to each image. It is recorded as an ASCII string equivalent to hexadecimal notation and 128-bit fixed length.'],
    42032: ['Exif.Photo.CameraOwnerName', 'Ascii', 'This tag records the owner of a camera used in photography as an ASCII string.'],
    42033: ['Exif.Photo.BodySerialNumber', 'Ascii', 'This tag records the serial number of the body of the camera that was used in photography as an ASCII string.'],
    42034: ['Exif.Photo.LensSpecification', 'Rational', 'This tag notes minimum focal length, maximum focal length, minimum F number in the minimum focal length, and minimum F number in the maximum focal length, which are specification information for the lens that was used in photography. When the minimum F number is unknown, the notation is 0/0'],
    42035: ['Exif.Photo.LensMake', 'Ascii', 'This tag records the lens manufactor as an ASCII string.'],
    42036: ['Exif.Photo.LensModel', 'Ascii', "This tag records the lens's model name and model number as an ASCII string."],
    42037: ['Exif.Photo.LensSerialNumber', 'Ascii', 'This tag records the serial number of the interchangeable lens that was used in photography as an ASCII string.'],
    42038: ['Exif.Photo.ImageTitle', 'Ascii', 'This tag records the title of the image.'],
    42039: ['Exif.Photo.Photographer', 'Ascii', 'This tag records the name of the photographer.'],
    42040: ['Exif.Photo.ImageEditor', 'Ascii', 'This tag records the name of the main person who edited the image. Preferably, a single name is written (individual name, group/organization name, etc.), but multiple main editors may be entered.'],
    42041: ['Exif.Photo.CameraFirmware', 'Ascii', 'This tag records the name and version of the software or firmware of the camera used to generate the image.'],
    42042: ['Exif.Photo.RAWDevelopingSoftware', 'Ascii', 'This tag records the name and version of the software used to develop the RAW image.'],
    42043: ['Exif.Photo.ImageEditingSoftware', 'Ascii', 'This tag records the name and version of the main software used for processing and editing the image. Preferably, a single software is written, but multiple main software may be entered.'],
    42044: ['Exif.Photo.MetadataEditingSoftware', 'Ascii', 'This tag records the name and version of one software used to edit the metadata of the image without processing or editing of the image data itself.'],
    42080: ['Exif.Photo.CompositeImage', 'Short', 'Indicates whether the recorded image is a composite image or not.'],
    42081: ['Exif.Photo.SourceImageNumberOfCompositeImage', 'Short', 'Indicates the number of the source images (tentatively recorded images) captured for a composite Image.'],
    42082: ['Exif.Photo.SourceExposureTimesOfCompositeImage', 'Undefined', 'For a composite image, records the parameters relating exposure time of the exposures for generating the said composite image, such as respective exposure times of captured source images (tentatively recorded images).'],
    42240: ['Exif.Photo.Gamma', 'Rational', 'Indicates the value of coefficient gamma. The formula of transfer function used for image reproduction is expressed as follows: (reproduced value) = (input value)^gamma. Both reproduced value and input value indicate normalized value, whose minimum value is 0 and maximum value is 1.'],
    45056: ['Exif.MpfInfo.MPFVersion', 'Ascii', 'MPF Version'],
    45057: ['Exif.MpfInfo.MPFNumberOfImages', 'Undefined', 'MPF Number of Images'],
    45058: ['Exif.MpfInfo.MPFImageList', 'Ascii', 'MPF Image List'],
    45059: ['Exif.MpfInfo.MPFImageUIDList', 'Long', 'MPF Image UID List'],
    45060: ['Exif.MpfInfo.MPFTotalFrames', 'Long', 'MPF Total Frames'],
    45313: ['Exif.MpfInfo.MPFIndividualNum', 'Long', 'MPF Individual Num'],
    45569: ['Exif.MpfInfo.MPFPanOrientation', 'Long', 'MPFPanOrientation'],
    45570: ['Exif.MpfInfo.MPFPanOverlapH', 'Long', 'MPF Pan Overlap Horizontal'],
    45571: ['Exif.MpfInfo.MPFPanOverlapV', 'Long', 'MPF Pan Overlap Vertical'],
    45572: ['Exif.MpfInfo.MPFBaseViewpointNum', 'Long', 'MPF Base Viewpoint Number'],
    45573: ['Exif.MpfInfo.MPFConvergenceAngle', 'Long', 'MPF Convergence Angle'],
    45574: ['Exif.MpfInfo.MPFBaselineLength', 'Long', 'MPF Baseline Length'],
    45575: ['Exif.MpfInfo.MPFVerticalDivergence', 'Long', 'MPF Vertical Divergence'],
    45576: ['Exif.MpfInfo.MPFAxisDistanceX', 'Long', 'MPF Axis Distance X'],
    45577: ['Exif.MpfInfo.MPFAxisDistanceY', 'Long', 'MPF Axis Distance Y'],
    45578: ['Exif.MpfInfo.MPFAxisDistanceZ', 'Long', 'MPF Axis Distance Z'],
    45579: ['Exif.MpfInfo.MPFYawAngle', 'Long', 'MPF Yaw Angle'],
    45580: ['Exif.MpfInfo.MPFPitchAngle', 'Long', 'MPF Pitch Angle'],
    45581: ['Exif.MpfInfo.MPFRollAngle', 'Long', 'MPF Roll Angle'],
}

NOMS_GPS = {
    0: ['Exif.GPSInfo.GPSVersionID', 'Byte', 'Indicates the version of <GPSInfoIFD>. The version is given as 2.0.0.0. This tag is mandatory when <GPSInfo> tag is present. (Note: The <GPSVersionID> tag is given in bytes, unlike the <ExifVersion> tag. When the version is 2.0.0.0, the tag value is 02000000.H).'],
    1: ['Exif.GPSInfo.GPSLatitudeRef', 'Ascii', "Indicates whether the latitude is north or south latitude. The ASCII value 'N' indicates north latitude, and 'S' is south latitude."],
    2: ['Exif.GPSInfo.GPSLatitude', 'Rational', 'Indicates the latitude. The latitude is expressed as three RATIONAL values giving the degrees, minutes, and seconds, respectively. When degrees, minutes and seconds are expressed, the format is dd/1,mm/1,ss/1. When degrees and minutes are used and, for example, fractions of minutes are given up to two decimal places, the format is dd/1,mmmm/100,0/1.'],
    3: ['Exif.GPSInfo.GPSLongitudeRef', 'Ascii', "Indicates whether the longitude is east or west longitude. ASCII 'E' indicates east longitude, and 'W' is west longitude."],
    4: ['Exif.GPSInfo.GPSLongitude', 'Rational', 'Indicates the longitude. The longitude is expressed as three RATIONAL values giving the degrees, minutes, and seconds, respectively. When degrees, minutes and seconds are expressed, the format is ddd/1,mm/1,ss/1. When degrees and minutes are used and, for example, fractions of minutes are given up to two decimal places, the format is ddd/1,mmmm/100,0/1.'],
    5: ['Exif.GPSInfo.GPSAltitudeRef', 'Byte', 'Indicates the altitude used as the reference altitude. If the reference is sea level and the altitude is above sea level, 0 is given. If the altitude is below sea level, a value of 1 is given and the altitude is indicated as an absolute value in the GSPAltitude tag. The reference unit is meters. Note that this tag is BYTE type, unlike other reference tags.'],
    6: ['Exif.GPSInfo.GPSAltitude', 'Rational', 'Indicates the altitude based on the reference in GPSAltitudeRef. Altitude is expressed as one RATIONAL value. The reference unit is meters.'],
    7: ['Exif.GPSInfo.GPSTimeStamp', 'Rational', 'Indicates the time as UTC (Coordinated Universal Time). <TimeStamp> is expressed as three RATIONAL values giving the hour, minute, and second (atomic clock).'],
    8: ['Exif.GPSInfo.GPSSatellites', 'Ascii', 'Indicates the GPS satellites used for measurements. This tag can be used to describe the number of satellites, their ID number, angle of elevation, azimuth, SNR and other information in ASCII notation. The format is not specified. If the GPS receiver is incapable of taking measurements, value of the tag is set to NULL.'],
    9: ['Exif.GPSInfo.GPSStatus', 'Ascii', 'Indicates the status of the GPS receiver when the image is recorded. "A" means measurement is in progress, and "V" means the measurement is Interoperability.'],
    10: ['Exif.GPSInfo.GPSMeasureMode', 'Ascii', 'Indicates the GPS measurement mode. "2" means two-dimensional measurement and "3" means three-dimensional measurement is in progress.'],
    11: ['Exif.GPSInfo.GPSDOP', 'Rational', 'Indicates the GPS DOP (data degree of precision). An HDOP value is written during two-dimensional measurement, and PDOP during three-dimensional measurement.'],
    12: ['Exif.GPSInfo.GPSSpeedRef', 'Ascii', 'Indicates the unit used to express the GPS receiver speed of movement. "K" "M" and "N" represents kilometers per hour, miles per hour, and knots.'],
    13: ['Exif.GPSInfo.GPSSpeed', 'Rational', 'Indicates the speed of GPS receiver movement.'],
    14: ['Exif.GPSInfo.GPSTrackRef', 'Ascii', 'Indicates the reference for giving the direction of GPS receiver movement. "T" denotes true direction and "M" is magnetic direction.'],
    15: ['Exif.GPSInfo.GPSTrack', 'Rational', 'Indicates the direction of GPS receiver movement. The range of values is from 0.00 to 359.99.'],
    16: ['Exif.GPSInfo.GPSImgDirectionRef', 'Ascii', 'Indicates the reference for giving the direction of the image when it is captured. "T" denotes true direction and "M" is magnetic direction.'],
    17: ['Exif.GPSInfo.GPSImgDirection', 'Rational', 'Indicates the direction of the image when it was captured. The range of values is from 0.00 to 359.99.'],
    18: ['Exif.GPSInfo.GPSMapDatum', 'Ascii', 'Indicates the geodetic survey data used by the GPS receiver. If the survey data is restricted to Japan, the value of this tag is "TOKYO" or "WGS-84".'],
    19: ['Exif.GPSInfo.GPSDestLatitudeRef', 'Ascii', 'Indicates whether the latitude of the destination point is north or south latitude. The ASCII value "N" indicates north latitude, and "S" is south latitude.'],
    20: ['Exif.GPSInfo.GPSDestLatitude', 'Rational', 'Indicates the latitude of the destination point. The latitude is expressed as three RATIONAL values giving the degrees, minutes, and seconds, respectively. If latitude is expressed as degrees, minutes and seconds, a typical format would be dd/1,mm/1,ss/1. When degrees and minutes are used and, for example, fractions of minutes are given up to two decimal places, the format would be dd/1,mmmm/100,0/1.'],
    21: ['Exif.GPSInfo.GPSDestLongitudeRef', 'Ascii', 'Indicates whether the longitude of the destination point is east or west longitude. ASCII "E" indicates east longitude, and "W" is west longitude.'],
    22: ['Exif.GPSInfo.GPSDestLongitude', 'Rational', 'Indicates the longitude of the destination point. The longitude is expressed as three RATIONAL values giving the degrees, minutes, and seconds, respectively. If longitude is expressed as degrees, minutes and seconds, a typical format would be ddd/1,mm/1,ss/1. When degrees and minutes are used and, for example, fractions of minutes are given up to two decimal places, the format would be ddd/1,mmmm/100,0/1.'],
    23: ['Exif.GPSInfo.GPSDestBearingRef', 'Ascii', 'Indicates the reference used for giving the bearing to the destination point. "T" denotes true direction and "M" is magnetic direction.'],
    24: ['Exif.GPSInfo.GPSDestBearing', 'Rational', 'Indicates the bearing to the destination point. The range of values is from 0.00 to 359.99.'],
    25: ['Exif.GPSInfo.GPSDestDistanceRef', 'Ascii', 'Indicates the unit used to express the distance to the destination point. "K", "M" and "N" represent kilometers, miles and nautical miles.'],
    26: ['Exif.GPSInfo.GPSDestDistance', 'Rational', 'Indicates the distance to the destination point.'],
    27: ['Exif.GPSInfo.GPSProcessingMethod', 'Comment', 'A character string recording the name of the method used for location finding. The string encoding is defined using the same scheme as UserComment.'],
    28: ['Exif.GPSInfo.GPSAreaInformation', 'Comment', 'A character string recording the name of the GPS area.The string encoding is defined using the same scheme as UserComment.'],
    29: ['Exif.GPSInfo.GPSDateStamp', 'Ascii', 'A character string recording date and time information relative to UTC (Coordinated Universal Time). The format is "YYYY:MM:DD.".'],
    30: ['Exif.GPSInfo.GPSDifferential', 'Short', 'Indicates whether differential correction is applied to the GPS receiver.'],
    31: ['Exif.GPSInfo.GPSHPositioningError', 'Rational', 'This tag indicates horizontal positioning errors in meters.'],
}


class Infos(Toplevel):
    def __init__(self, master, donnees):
        super().__init__(master)
        self.title("Infos supplémentaires")

        ligne = 0
        for nom in donnees:
            Label(self, text=nom).grid(row=ligne, column=0)
            Label(self, text=donnees[nom], wraplength=600).grid(row=ligne, column=1)
            ligne += 1


class GPSInfos(Toplevel):
    def __init__(self, master, donnees):
        super().__init__(master)
        self.title("Données GPS")
        
        Button(self, text="Voir sur une carte", command=self.ouvrir).pack()

        self.affiche = Treeview(self, columns=("nom", "valeur"))
        self.affiche.heading("#0", text="Id")
        self.affiche.heading("nom", text="Nom")
        self.affiche.heading("valeur", text="Valeur")
        scroll = Scrollbar(self, orient="vertical", command=self.affiche.yview)
        self.affiche.config(yscrollcommand=scroll.set)
        self.affiche.pack(side="left")
        scroll.pack(side="left", fill="y")

        self.meta = donnees
        for k in self.meta:
            try:
                self.affiche.insert("", "end", text=k, values=(NOMS_GPS[k][0], self.meta[k]))
            except KeyError:
                pass
        
        self.affiche.bind("<Double-1>", self.infos)
        
    def ouvrir(self):
        x, y = self.meta[2], self.meta[4]
        xd, yd = x[0] + x[1]/60 + x[2]/3600, y[0] + y[1]/60 + y[2]/3600
        xd, yd = float(xd), float(yd)
        if self.meta[1] == "S":
            xd *= -1
        if self.meta[3] == "W":
            yd *= -1
        webbrowser.open("https://www.openstreetmap.org/export/embed.html?"
                        f"bbox={yd-0.01},{xd-0.01},"
                        f"{yd+0.01},{xd+0.01}&layer=mapnik&"
                        f"marker={xd},{yd}")
    
    def infos(self, _):
        i = self.affiche.item(self.affiche.selection()[0], "text")
        affiche = {
            "Nom": NOMS_GPS[i][0],
            "Description": NOMS_GPS[i][2],
            "Valeur": self.meta[i]
        }
        Infos(self, affiche).mainloop()


class Fen(Tk):
    def __init__(self):
        super().__init__()
        self.title("Métadonnées exif")

        f = Frame(self)
        f.pack()
        Button(f, text="ouvrir", command=self.ouvrir).pack(side="left")
#        Button(f, text="exporter", command=self.exporter).pack(side="left")
        self.zone_pages = Frame(self)
        self.zone_pages.pack()

    def ouvrir(self):
        file = askopenfilename(filetypes=(("fichiers image", "*.png *.jpg *.jpeg"), ("tous les fichiers", "*.*")), title="Sélectionnez un fichier à importer", initialdir="e:/")
        if not file: return
        image = Image.open(file)
        
        self.affiche = Treeview(self, columns=("nom", "valeur"))
        self.affiche.heading("#0", text="Id")
        self.affiche.heading("nom", text="Nom")
        self.affiche.heading("valeur", text="Valeur")
        scroll = Scrollbar(self, orient="vertical", command=self.affiche.yview)
        self.affiche.config(yscrollcommand=scroll.set)
        self.affiche.pack(side="left")
        scroll.pack(side="left", fill="y")

        self.meta = image._getexif()
        for k in self.meta:
            try:
                self.affiche.insert("", "end", text=k, values=(NOMS[k][0], self.meta[k]))
            except KeyError:
                pass
        
        self.affiche.bind("<Double-1>", self.infos)
    
    def infos(self, _):
        i = self.affiche.item(self.affiche.selection()[0], "text")
        if i != 34853:
            affiche = {
                "Nom": NOMS[i][0],
                "Description": NOMS[i][2],
                "Valeur": self.meta[i]
            }
            Infos(self, affiche).mainloop()
        else:
            GPSInfos(self, self.meta[i])
    
    def exporter(self):
        file = asksaveasfilename(filetypes=(("fichiers texte", "*.txt"), ("tous les fichiers", "*.*")), title="Sélectionnez le fichier de destination", initialfile="metadonnées", defaultextension="txt")
        if not file: return
        ...


if __name__ == "__main__":
    Fen().mainloop()
