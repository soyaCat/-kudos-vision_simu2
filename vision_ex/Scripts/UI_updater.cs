using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UI_updater : MonoBehaviour
{
    public GameObject handleRobot;
    public GameObject cameraPack;
    public GameObject Canvas_Text;
    private Text information_board;
    private string information;
    private Vector3 handleRobot_pos;
    private Vector3 handleRobot_lot;
    private Vector3 cameraPack_lot;
    // Start is called before the first frame update
    void Start()
    {
        handleRobot_pos = handleRobot.transform.position;
        handleRobot_lot = handleRobot.transform.eulerAngles;
        cameraPack_lot = cameraPack.transform.eulerAngles;
        cameraPack_lot.y = get_camera_lot(handleRobot_lot.y, cameraPack_lot.y);
        information_board = Canvas_Text.GetComponent<Text>();
        information = "RP: " + handleRobot_pos.ToString() + "\n" +
                        "RL: " + handleRobot_lot.ToString() + "\n" +
                        "RCL: " + cameraPack_lot.ToString();
        information_board.text = information;
    }

    // Update is called once per frame
    void Update()
    {
        handleRobot_pos = handleRobot.transform.position;
        handleRobot_lot = handleRobot.transform.eulerAngles;
        cameraPack_lot = cameraPack.transform.eulerAngles;
        cameraPack_lot.y = get_camera_lot(handleRobot_lot.y, cameraPack_lot.y);
        information = "RP: " + handleRobot_pos.ToString() + "\n" +
                        "RL: " + handleRobot_lot.ToString() + "\n" +
                        "RCL: " + cameraPack_lot.ToString();
        information_board.text = information;
    }

    private float get_camera_lot(float robot_lot, float camera_lot)
    {
        var distance_lot = robot_lot - camera_lot;
        if (Mathf.Abs(distance_lot)< 180f)
        {
            camera_lot = camera_lot - robot_lot;
        }
        else
        {
            if(robot_lot > camera_lot)
            {
                camera_lot = camera_lot + 360f;
                camera_lot = camera_lot - robot_lot;
            }
            else
            {
                robot_lot = robot_lot + 360f;
                camera_lot = camera_lot - robot_lot;
            }
        }
        return camera_lot;
    }
}
