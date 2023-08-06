import requests

try:
    from robot.libraries.BuiltIn import BuiltIn
    from robot.libraries.BuiltIn import _Misc
    import robot.api.logger as logger
    from robot.api.deco import keyword
    ROBOT = False
except Exception:
    ROBOT = False

def trackusageMinimal(projectName, UserName, RunEnvironment, CRQRequest, Squad, tracking_ttl_testcases):
    proj_name = projectName
    username = UserName
    ttl_testcases_run = tracking_ttl_testcases
    env = RunEnvironment
    crq = CRQRequest
    squad = Squad

  # send REQ
    url ="https://automateher.azurewebsites.net/api/Tracking/TrackProjectCounter?proj="+proj_name+"&username="+username+"&ttl_testcases_run=+"+ttl_testcases_run+"+&env="+env+"+&crq="+crq+"+&squad="+squad
    resp = requests.get(url, timeout=10000)

    BuiltIn().log_to_console(f"Response Code: {resp.status_code}, Response: {resp.text}")
    BuiltIn().log_to_console(f"Response Data: {resp.text}")

    return resp


def trackusageFull(projectName, UserName, RunEnvironment, CRQRequest, Squad, tracking_ttl_testcases, tracking_testcases_executed, tracking_testcases_passed, tracking_testcases_failed, tracking_testcases_blocked, tracking_testcases_norun, tracking_testcases_notcompleted, tracking_critical_defects, tracking_major_defects, tracking_medium_defects, tracking_low_defects, tracking_automated_tests, tracking_manual_tests, tracking_non_functional_tests, tracking_test_result_img, tracking_subject_status_img, tracking_test_by_testers_img, tracking_test_type ):
   
    #send REQ
    url ="https://automateher.azurewebsites.net/api/Tracking/TrackProjectCounter?proj="+projectName+"&username="+UserName+"&ttl_testcases_run=+"+tracking_ttl_testcases+"+&env="+RunEnvironment+"+&crq="+CRQRequest+"+&squad="+Squad+"+&executed_testcases="+tracking_testcases_executed+"+&passed_testcases="+tracking_testcases_passed+"+&failed_testcases="+tracking_testcases_failed+"+&blocked_testcases="+tracking_testcases_blocked+"+&norun_testcases="+tracking_testcases_norun+"+&notcompleted_testcases="+tracking_testcases_notcompleted+"+&critical_defects="+tracking_critical_defects+"+&major_defects="+tracking_major_defects+"+&medium_defects="+tracking_medium_defects+"+&low_defects="+tracking_low_defects+"+&automated_tests="+tracking_automated_tests+"+&manual_tests="+tracking_manual_tests+"+&functional_tests="+tracking_non_functional_tests+"+&res_img="+tracking_test_result_img+"+&stat_img="+tracking_subject_status_img+"+&testers_img="+tracking_test_by_testers_img+"+&test_type="+tracking_test_type
    resp = requests.get(url, timeout=10000)
    
    return resp

