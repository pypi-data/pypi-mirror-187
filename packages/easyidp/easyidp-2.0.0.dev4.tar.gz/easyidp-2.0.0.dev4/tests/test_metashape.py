import re
import pytest
import pyproj
import numpy as np
import xml.etree.ElementTree as ET

import easyidp as idp


test_data = idp.data.TestData()

#########################
# test math calculation #
#########################
def test_apply_transform_matrix():
    matrix = np.asarray([
        [-0.86573098, -0.01489186,  0.08977677,  7.65034123],
        [ 0.06972335,  0.44334391,  0.74589315,  1.85910928],
        [-0.05848325,  0.74899678, -0.43972184, -0.1835615],
        [ 0.,          0.,          0.,          1.]], dtype=np.float)
    matrix2 = np.linalg.inv(matrix)

    point1 = np.array([0.5, 1, 1.5], dtype=np.float)
    out1 = idp.metashape.apply_transform_matrix(point1, matrix2)

    ans1 = np.array([7.96006409,  1.30195288, -2.66971818])
    np.testing.assert_array_almost_equal(out1, ans1, decimal=6)

    np_array = np.array([
        [0.5, 1, 1.5],
        [0.5, 1, 1.5]], dtype=np.float)
    out2 = idp.metashape.apply_transform_matrix(np_array, matrix2)
    ans2 = np.array([
        [7.96006409, 1.30195288, -2.66971818],
        [7.96006409, 1.30195288, -2.66971818]])
    np.testing.assert_array_almost_equal(out2, ans2, decimal=6)


def test_convert_proj3d():
    # transform between geocentric and geodetic
    geocentric = np.array([-3943658.7087006606, 3363404.124223561, 3704651.3067566575])

    # columns=['lon', 'lat', 'alt']
    geodetic = np.array([139.54033578028609, 35.73756358928734, 96.87827569602781])

    geo_d = pyproj.CRS.from_epsg(4326)
    geo_c = pyproj.CRS.from_dict({"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'})

    out_c = idp.geotools.convert_proj3d(
        geodetic, geo_d, geo_c, is_xyz=True
    )
    # x: array([[-3943658.715, 3363404.132, 3704651.343]])
    # y: array([[-3943658.709, 3363404.124, 3704651.307]])
    np.testing.assert_array_almost_equal(out_c, geocentric, decimal=1)

    out_d = idp.geotools.convert_proj3d(
        geocentric, geo_c, geo_d, is_xyz=False
    )
    # x: array([[139.540336,  35.737563,  96.849   ]])
    # y: array([[139.540336,  35.737564,  96.878276]])
    np.testing.assert_array_almost_equal(out_d[0:2], geodetic[0:2], decimal=5)
    np.testing.assert_array_almost_equal(out_d[2], geodetic[2], decimal=1)

############################
# test metashape functions #
############################

def test_read_chunk_zip_label_only():

    out_dict = idp.metashape.read_chunk_zip(
        str(test_data.metashape.lotus_psx)[:-9], "Lotus", chunk_id=0, return_label_only=True)

    assert list(out_dict.keys()) == ['label','enabled']

#########################
# test metashape object #
#########################
def test_class_init_metashape():
    m1 = idp.Metashape()
    assert m1.software == "metashape"

    # load with project_path
    m2 = idp.Metashape(project_path=test_data.metashape.goya_psx)
    assert m2.project_name == "goya_test"
    assert m2.label == 'Chunk 1'

    # load with project_path + chunk_id
    m2 = idp.Metashape(project_path=test_data.metashape.goya_psx, chunk_id=0)
    assert m2.project_name == "goya_test"
    ## check values
    assert m2.label == 'Chunk 1'
    assert m2.meta == {}
    assert len(m2.photos) == 259
    assert m2.photos[0].label == "DJI_0284.JPG"
    assert m2.photos[0].enabled == True
    assert m2.photos[0].path == "//172.31.12.56/pgg2020a/drone/20201029/goya/DJI_0284.JPG"
    assert m2.photos[0].rotation.shape == (3, 3)
    assert m2.photos[0].sensor.width == m2.sensors[0].width

def test_class_init_metashape_warns_errors():
    # warning init with chunk_id without project_path
    with pytest.warns(UserWarning, match=re.escape("Unable to open chunk_id [0] for empty project with project_path=None")):
        m3 = idp.Metashape(chunk_id=0)

    # warning with multiple chunks:
    with pytest.warns(UserWarning, match=re.escape("The project has [4] chunks, however no chunk_id has been specified, open the first chunk [1] 'multiple_bbb' by default.")):
        m4 = idp.Metashape(project_path=test_data.metashape.multichunk_psx)

    # warning with unable for further anaylsys
    with pytest.warns(UserWarning, match=re.escape("Current chunk missing required ['transform', 'sensors', 'photos'] information (is it an empty chunk without finishing SfM tasks?) and unable to do further analysis.")):
        m4 = idp.Metashape(project_path=test_data.metashape.multichunk_psx, chunk_id=1)
        
    m4 = idp.Metashape(project_path=test_data.metashape.multichunk_psx)

    # trace errors for empty chunk:
    with pytest.raises(TypeError, match=re.escape("Unable to process disabled chunk (.enabled=False)")):
        m4.back2raw('roi')
    with pytest.raises(TypeError, match=re.escape("Unable to process disabled chunk (.enabled=False)")):
        m4.back2raw_crs('roi')
    with pytest.raises(TypeError, match=re.escape("Unable to process disabled chunk (.enabled=False)")):
        m4.get_photo_position('roi')
    with pytest.raises(TypeError, match=re.escape("Unable to process disabled chunk (.enabled=False)")):
        m4.sort_img_by_distance('img_dict_all', 'roi')

    # trace warnings when not given correct CRS
    m5 = idp.Metashape(test_data.metashape.lotus_psx)
    plot = np.ones((5,3)) * np.array([360000, 3950000, 100])

    with pytest.warns(UserWarning, match=re.escape("Have not specify the CRS of output DOM/DSM/PCD, ")):
        m5.back2raw_crs(plot)

    with pytest.warns(UserWarning, match=re.escape("Have not specify the CRS of output DOM/DSM/PCD, ")):
        roi = idp.ROI()
        roi['plot1'] = plot
        m5.back2raw(roi)
            

def test_class_fetch_by_label():
    m2 = idp.Metashape(project_path=test_data.metashape.goya_psx, chunk_id="Chunk 1")

    assert m2.label == 'Chunk 1'


def test_class_fetch_by_label_error():
    with pytest.raises(KeyError, match=re.escape("Could not find chunk_id [21] in")):
        m2 = idp.Metashape(project_path=test_data.metashape.multichunk_psx, chunk_id="21")

    with pytest.warns(UserWarning, match=re.escape("This project only has one chunk named [0] 'Chunk 1', ignore the wrong chunk_id [21] specified by user.")):
        m3 = idp.Metashape(project_path=test_data.metashape.goya_psx, chunk_id="21")

def test_class_show_chunk():
    m1 = idp.Metashape()

    assert m1._show_chunk() == "<Empty easyidp.Metashape object>"

    ms_goya = idp.Metashape(project_path=test_data.metashape.goya_psx)

    goya_show = \
        "<'goya_test.psx' easyidp.Metashape object with 1 active chunks>\n\n" \
        "  id  label\n" \
        "----  -------\n" \
        "-> 0  Chunk 1"

    assert ms_goya._show_chunk().replace(' ', '') == goya_show.replace(' ', '')

    ms_lotus = idp.Metashape(project_path=test_data.metashape.lotus_psx)

    lotus_show = \
        "<'Lotus.psx' easyidp.Metashape object with 1 active chunks>\n\n" \
        "  id  label\n" \
        "----  -------\n" \
        "-> 0  Chunk 1"

    assert ms_lotus._show_chunk().replace(' ', '') == lotus_show.replace(' ', '')

    m4 = idp.Metashape(project_path=test_data.metashape.multichunk_psx, chunk_id=1)
    m4_show = \
        "<'multichunk.psx' easyidp.Metashape object with 4 active chunks>\n\n" \
        "  id  label\n" \
        "----  --------------\n" \
        "-> 1  multiple_bbb\n" \
        "   2  multiple_aaa\n" \
        "   3  multiple_aaa_1\n" \
        "   4  multiple_aaa_2"
    
    assert m4._show_chunk().replace(' ', '') == m4_show.replace(' ', '')

    # test the ability to handle duplicated name
    assert list(m4._label2chunk_id.keys()) == list(m4._chunk_id2label.values())
    assert list(m4._label2chunk_id.values()) == list(m4._chunk_id2label.keys())

def test_class_open_chunk_print():

    m4 = idp.Metashape(project_path=test_data.metashape.multichunk_psx, chunk_id=1)

    # open chunk by id
    m4.open_chunk('4')
    m4_show_id = \
        "<'multichunk.psx' easyidp.Metashape object with 4 active chunks>\n\n" \
        "  id  label\n" \
        "----  --------------\n" \
        "   1  multiple_bbb\n" \
        "   2  multiple_aaa\n" \
        "   3  multiple_aaa_1\n" \
        "-> 4  multiple_aaa_2"
    
    assert m4._show_chunk().replace(' ', '') == m4_show_id.replace(' ', '')

    # open chunk by label
    m4.open_chunk('multiple_aaa')
    m4_show_label = \
        "<'multichunk.psx' easyidp.Metashape object with 4 active chunks>\n\n" \
        "  id  label\n" \
        "----  --------------\n" \
        "   1  multiple_bbb\n" \
        "-> 2  multiple_aaa\n" \
        "   3  multiple_aaa_1\n" \
        "   4  multiple_aaa_2"
    
    assert m4._show_chunk().replace(' ', '') == m4_show_label.replace(' ', '')

def test_local2world2local():
    attempt1 = idp.Metashape()
    attempt1.transform.matrix = np.asarray([
        [-0.86573098, -0.01489186,  0.08977677,  7.65034123],
        [ 0.06972335,  0.44334391,  0.74589315,  1.85910928],
        [-0.05848325,  0.74899678, -0.43972184, -0.1835615],
        [ 0.,          0.,          0.,           1.]], dtype=np.float)
    w_pos = np.array([0.5, 1, 1.5])
    l_pos = np.array(
        [7.960064093299587, 1.3019528769064523, -2.6697181763370965]
    )
    w_pos_ans = np.array(
        [0.4999999999999978, 0.9999999999999993, 1.5]
    )

    world_pos = attempt1._local2world(l_pos)
    np.testing.assert_array_almost_equal(w_pos_ans, world_pos, decimal=6)

    local_pos = attempt1._world2local(w_pos)
    np.testing.assert_array_almost_equal(l_pos, local_pos, decimal=6)


def test_metashape_project_local_points_on_raw():
    chunk = idp.Metashape(test_data.metashape.goya_psx, chunk_id=0)

    # test for single point
    l_pos = np.array([7.960064093299587, 1.3019528769064523, -2.6697181763370965])

    p_dis_out = chunk._back2raw_one2one(
        l_pos, photo_id=0, distortion_correct=False)
    p_undis_out = chunk._back2raw_one2one(
        l_pos, photo_id=0, distortion_correct=True)

    # pro_api_out = np.asarray([2218.883386793118, 1991.4709388015149])
    my_undistort_out = np.array([2220.854889556147, 1992.6933680261686])
    my_distort_out = np.array([2218.47960556, 1992.46356322])

    np.testing.assert_array_almost_equal(p_dis_out, my_distort_out)
    np.testing.assert_array_almost_equal(p_undis_out, my_undistort_out)

    # test for multiple points
    l_pos_points = np.array([
        [7.960064093299587, 1.3019528769064523, -2.6697181763370965],
        [7.960064093299587, 1.3019528769064523, -2.6697181763370965]])

    p_dis_outs = chunk._back2raw_one2one(
        l_pos_points, photo_id=0, distortion_correct=False)
    p_undis_outs = chunk._back2raw_one2one(
        l_pos_points, photo_id=0, distortion_correct=True)

    my_undistort_outs = np.array([
        [2220.854889556147, 1992.6933680261686],
        [2220.854889556147, 1992.6933680261686]])
    my_distort_outs = np.array([
        [2218.47960556, 1992.46356322],
        [2218.47960556, 1992.46356322]])

    np.testing.assert_array_almost_equal(p_dis_outs, my_distort_outs)
    np.testing.assert_array_almost_equal(p_undis_outs, my_undistort_outs)


def test_world2crs_and_on_raw_images():
    chunk = idp.Metashape(test_data.metashape.wheat_psx, chunk_id=0)

    local = np.array(
        [11.870130675203006, 0.858098777517136, -12.987136541275])
    geocentric = np.array(
        [-3943658.7087006606, 3363404.124223561, 3704651.3067566575])
    # columns=['lon', 'lat', 'alt']
    geodetic = np.array(
        [139.54033578028609, 35.73756358928734, 96.87827569602781])

    idp_world = chunk._local2world(local)
    np.testing.assert_array_almost_equal(idp_world, geocentric, decimal=1)

    idp_crs = chunk._world2crs(idp_world)
    np.testing.assert_array_almost_equal(idp_crs, geodetic)

    camera_id = 56
    camera_label = "DJI_0057"
    camera_pix_ans = np.array([2391.7104647010146, 1481.8987733175165])

    idp_cam_pix = chunk._back2raw_one2one(local, camera_id, distortion_correct=True)
    np.testing.assert_array_almost_equal(camera_pix_ans, idp_cam_pix)

    idp_cam_pix_l = chunk._back2raw_one2one(local, camera_label, distortion_correct=True)
    np.testing.assert_array_almost_equal(camera_pix_ans, idp_cam_pix_l)


def test_class_back2raw_and_crs():
    ms = idp.Metashape(project_path=test_data.metashape.lotus_psx, chunk_id=0)

    roi = idp.ROI(test_data.shp.lotus_shp, name_field=0)
    # only pick 2 plots as testing data
    key_list = list(roi.keys())
    for key in key_list:
        if key not in ["N1W1", "N1W2"]:
            del roi[key]
    roi.get_z_from_dsm(test_data.metashape.lotus_dsm)

    poly = roi["N1W2"]
    ms.crs = roi.crs

    out = ms.back2raw_crs(poly)

    assert len(out) == 21

    out_all = ms.back2raw(roi)

    assert len(out_all) == 2
    assert isinstance(out_all["N1W2"], dict)


def test_class_back2raw_error():
    ms = idp.Metashape(test_data.metashape.lotus_psx)

    roi = idp.ROI(test_data.shp.lotus_shp, name_field=0)

    with pytest.raises(
        ValueError, 
        match=re.escape(
            "The back2raw function requires 3D roi with shape=(n, 3), but [N1W1] is (5, 2)")):
            ms.back2raw(roi)


def test_metashape_get_photo_position():
    lotus = idp.data.Lotus()
    ms = idp.Metashape(lotus.metashape.project, chunk_id=0)

    out = ms.get_photo_position()

    assert len(out) == 151
    assert "DJI_0430" in out.keys()
    np.testing.assert_almost_equal(out["DJI_0430"], np.array([139.5405732 ,  35.73445975, 128.96422715]))
    
    # convert to another proj
    out_utm = ms.get_photo_position(pyproj.CRS.from_epsg(32654), refresh=True)
    np.testing.assert_almost_equal(out_utm['DJI_0430'], np.array([ 368021.21565782, 3955478.61203427,     128.96422715]))

    # change crs and refresh
    ms.crs = pyproj.CRS.from_epsg(32654)
    assert ms._photo_position_cache is None
    out_utm = ms.get_photo_position()
    np.testing.assert_almost_equal(out_utm['DJI_0430'], np.array([ 368021.21565782, 3955478.61203427,     128.96422715]))


def test_debug_discussion_12():
    ms = idp.Metashape()

    pos = np.array([-3943837.80419438,  3363533.48603071,  3704402.1784295 ])
    ms.crs = pyproj.CRS.from_epsg(32654)

    '''
    The following code will raise the following error:

    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "D:\OneDrive\Program\GitHub\EasyIDP\easyidp\metashape.py", line 99, in _world2crs
        return convert_proj3d(points_np, self.world_crs, self.crs)
      File "D:\OneDrive\Program\GitHub\EasyIDP\easyidp\metashape.py", line 1047, in convert_proj3d
        return out[0, :]
    raise UnboundLocalError: local variable 'out' referenced before assignment

    Reasons:
    is_xyz = True -> crs_target(epsg32654) neither is_geocentric nor is_geographic, it is `is_projected`

    <Derived Projected CRS: EPSG:32654>
    Name: WGS 84 / UTM zone 54N
    Axis Info [cartesian]:
    - E[east]: Easting (metre)
    - N[north]: Northing (metre)
    Area of Use:
    - name: Between 138°E and 144°E, northern hemisphere between equator and 84°N, onshore and offshore. Japan. Russian Federation.
    - bounds: (138.0, 0.0, 144.0, 84.0)
    Coordinate Operation:
    - name: UTM zone 54N
    - method: Transverse Mercator
    Datum: World Geodetic System 1984 ensemble
    - Ellipsoid: WGS 84
    - Prime Meridian: Greenwich
    '''
    #with pytest.raises(TypeError, match=re.escape("Given crs is neither `crs.is_geocentric=True` nor `crs.is_geographic`")):
    
    out = ms._world2crs(pos)
    np.testing.assert_almost_equal(out, np.array([ 368017.73174354, 3955492.19259721,     130.09433649]))

    back = ms._crs2world(out)
    np.testing.assert_almost_equal(back, pos)

    ms.crs = None

    out = ms._world2crs(pos)
    np.testing.assert_almost_equal(out, np.array([139.54053245,  35.73458169, 130.09433649]))

def test_debug_calibration_tag_error():
    # test ishii san's <calibration> out of index error (has one sensor tag without <calibration>)
    wrong_sensor = """
    <sensors next_id="2">
        <sensor id="0" label="Test_Pro (10.26mm)" type="frame">
            <resolution width="5472" height="3648"/>
            <property name="pixel_width" value="0.0024107142857142856"/>
            <property name="pixel_height" value="0.0024107142857142856"/>
            <property name="focal_length" value="10.26"/>
            <property name="layer_index" value="0"/>
            <bands>
                <band label="Red"/>
                <band label="Green"/>
                <band label="Blue"/>
            </bands>
            <data_type>uint8</data_type>
            <meta>
                <property name="Exif/BodySerialNumber" value="0K8TGAM0125288"/>
                <property name="Exif/Make" value="DJI"/>
                <property name="Exif/Model" value="Test_Pro"/>
                <property name="Exif/Software" value="10.00.11.04"/>
            </meta>
        </sensor>
        <sensor id="1" label="Test_Pro (10.26mm)" type="frame">
            <resolution width="5472" height="3648"/>
            <property name="pixel_width" value="0.0024107142857142856"/>
            <property name="pixel_height" value="0.0024107142857142856"/>
            <property name="focal_length" value="10.26"/>
            <property name="layer_index" value="0"/>
            <bands>
                <band label="Red"/>
                <band label="Green"/>
                <band label="Blue"/>
            </bands>
            <data_type>uint8</data_type>
            <calibration type="frame" class="adjusted">
                <resolution width="5472" height="3648"/>
                <f>3239.2350850187408</f>
                <cx>-17.266617222361305</cx>
                <cy>51.627079230267093</cy>
                <k1>-0.0061748904544724733</k1>
                <k2>0.0085312948846406767</k2>
                <k3>-0.0059426077261182687</k3>
                <p1>0.0038636434570336977</p1>
                <p2>0.00036559169480901107</p2>
            </calibration>
            <covariance>
                <params>f cx cy k1 k2 k3 p1 p2</params>
                <coeffs>1.3198921426619455e+02 -3.6441406803097598e-01 -8.8691870942484619e-01 -4.8035808438808746e-04 1.3837494678605588e-03 -1.4478477773082513e-03 1.6448496189504767e-04 1.9359169816499220e-05 -3.6441406803097598e-01 8.8492784732170038e-01 -1.8406731551178616e-02 4.5636954299254024e-06 -9.8824939561102722e-06 9.7826072595011059e-06 7.4748795744222678e-07 2.2077354984627524e-07 -8.8691870942484619e-01 -1.8406731551178616e-02 1.1190160084598506e+00 4.4433944809015497e-06 -1.4316737176840743e-05 1.3926778019564493e-05 -1.6128351018434475e-06 3.4438887312607803e-06 -4.8035808438808746e-04 4.5636954299254024e-06 4.4433944809015497e-06 3.2480428480148513e-09 -6.0445335360342845e-09 5.8919283699049205e-09 -5.4758330566968659e-10 -6.0991623945693416e-11 1.3837494678605588e-03 -9.8824939561102722e-06 -1.4316737176840743e-05 -6.0445335360342845e-09 1.7024280489663090e-08 -1.6861506240264254e-08 1.7186999180350537e-09 1.5819520020961357e-10 -1.4478477773082513e-03 9.7826072595011059e-06 1.3926778019564493e-05 5.8919283699049205e-09 -1.6861506240264254e-08 1.7046680052661823e-08 -1.7854037432768406e-09 -1.7316458740206863e-10 1.6448496189504767e-04 7.4748795744222678e-07 -1.6128351018434475e-06 -5.4758330566968659e-10 1.7186999180350537e-09 -1.7854037432768406e-09 7.4263922628734573e-10 2.0456928859553929e-11 1.9359169816499220e-05 2.2077354984627524e-07 3.4438887312607803e-06 -6.0991623945693416e-11 1.5819520020961357e-10 -1.7316458740206863e-10 2.0456928859553929e-11 5.5219741883705303e-10</coeffs>
            </covariance>
            <meta>
                <property name="Exif/BodySerialNumber" value="0K8TGAM0125288"/>
                <property name="Exif/Make" value="DJI"/>
                <property name="Exif/Model" value="Test_Pro"/>
                <property name="Exif/Software" value="10.00.11.04"/>
            </meta>
        </sensor>
    </sensors>
    """

    xml_tree = ET.ElementTree(ET.fromstring(wrong_sensor))
    for i, sensor_tag in enumerate(xml_tree.findall("./sensors/sensor")):

        if i == 0:
            with pytest.warns(UserWarning, match=re.escape("The sensor tag in [chunk_id/chunk.zip] has 0 <calibration> tags")):
                sensor = idp.metashape._decode_sensor_tag(sensor_tag)

            assert sensor.calibration is None
        else:
            sensor = idp.metashape._decode_sensor_tag(sensor_tag)

            assert sensor.calibration.f == 3239.2350850187408