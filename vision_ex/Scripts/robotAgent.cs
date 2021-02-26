using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class robotAgent : Agent
{
    public GameObject football_basic;
    public GameObject football_red;
    public GameObject football_blue;
    public GameObject football_green;
    public GameObject football_white;
    public GameObject football_marble;
    public GameObject ball_red;
    public GameObject ball_blue;
    public GameObject ball_sp1;
    public GameObject ball_sp2;
    public GameObject ball_sp3;
    public GameObject Soccer_Ball;
    public GameObject cameraPack;
    public GameObject lookAtTarget;
    public GameObject handleRobot;

    private List<GameObject> footballs = new List<GameObject>();

    void Start()
    {

    }


    public override void CollectObservations(VectorSensor sensor)
    {
        /*
        RaycastHit hit;
        float Angle;
        Ray ray;
        int rayCount = 27;
        List<Vector3> debugRay = new List<Vector3>();

        for (int i =0; i<=rayCount; i++)
        {
            Angle = i * Mathf.PI / rayCount;
            ray = new Ray(transform.position, new Vector3(0f, Mathf.Sin(Angle), Mathf.Cos(Angle)));
            if(Physics.Raycast(ray, out hit))
            {
                sensor.AddObservation(hit.distance);
                debugRay.Add(hit.point);
            }
        }
        for(int i = 0; i<debugRay.Count; i++)
        {
            Debug.DrawRay(transform.position, debugRay[i] - this.transform.position, Color.green);
        }
        */
    }

    public override void OnActionReceived(ActionBuffers actionBuffers)
    {
        var act0 = actionBuffers.DiscreteActions[0];
        var move_mode = actionBuffers.DiscreteActions[1];
        var head_horizen = actionBuffers.DiscreteActions[2];
        var head_vertical = actionBuffers.DiscreteActions[3];
        var nextPose = 0;
        var randomInt = Random.Range(0, footballs.Count());
        var randomLookAtPosition = new Vector3(0f, 0f, 0f);
        switch (act0)
        {
            case 1:
                nextPose = 1;//테스트 모드: 로봇과 오브젝트들의 위치가 고정됨
                break;
            case 2:
                nextPose = 2;//디폴트 모드:로봇과 공의 위치가 랜덤
                break;
            case 3:
                nextPose = 3;//조종 모드: 로봇을 파이썬에서 조종할수 있게 함
                break;
        }
        if(nextPose == 1)
        {
            Soccer_Ball.SetActive(false);
            for (int i = 0; i < footballs.Count(); i++)
            {
                if (i != randomInt)
                    footballs[i].gameObject.SetActive(false);
                else
                    footballs[i].gameObject.SetActive(true);
            }
            handleRobot.transform.position = new Vector3(0f, 2f, -7f);
            cameraPack.transform.eulerAngles = new Vector3(0f, 0f, 0f);
            footballs[randomInt].transform.position = new Vector3(0f, 0.5f, 0f);
            footballs[randomInt].transform.eulerAngles= new Vector3(Random.Range(0f,180f), Random.Range(0f,180f), Random.Range(0f,180f));
        }
        else if(nextPose == 2)
        {
            Soccer_Ball.SetActive(false);
            for (int i = 0; i < footballs.Count(); i++)
            {
                if (i != randomInt)
                    footballs[i].gameObject.SetActive(false);
                else 
                    footballs[i].gameObject.SetActive(true);
            }
            handleRobot.transform.position = new Vector3(Random.Range(-6f, 6f), 1.875f, Random.Range(-11f, 11f));
            if(move_mode == 0)//시선이 되도록 공 근처로 가도록 설정
            {
                var distance_Robot_ball = 8f;
                while(true)
                {
                    if (distance_Robot_ball >= 8f)
                    {
                        footballs[randomInt].transform.position = new Vector3(Random.Range(-6f, 6f), 0.5f, Random.Range(-11f, 11f));
                        footballs[randomInt].transform.eulerAngles = new Vector3(Random.Range(0f, 180f), Random.Range(0f, 180f), Random.Range(0f, 180f));
                        distance_Robot_ball = Vector3.Distance(handleRobot.transform.position, footballs[randomInt].transform.position);
                    }
                    else
                        break;
                }
                var Balldistance = Vector3.Distance(handleRobot.transform.position, footballs[randomInt].transform.position);
                randomLookAtPosition = footballs[randomInt].transform.position + new Vector3(Random.Range(-1f, 1f), 0f, Random.Range(-1f, 1f))*(Balldistance/2.3f);
            }
            else if(move_mode == 1)//시선을 공에 상관없이 아무데나 둠
            {
                footballs[randomInt].transform.position = new Vector3(Random.Range(-6f, 6f), 0.5f, Random.Range(-11f, 11f));
                randomLookAtPosition = new Vector3(Random.Range(-6f, 6f), 1.875f, Random.Range(-11f, 11f));
            }
            else if (move_mode == 2)//공이 엄청 가깝게 배치됨
            {
                var distance_Robot_ball = 2f;
                while (true)
                {
                    if (distance_Robot_ball >= 2f)
                    {
                        footballs[randomInt].transform.position = new Vector3(Random.Range(-6f, 6f), 0.5f, Random.Range(-11f, 11f));
                        footballs[randomInt].transform.eulerAngles = new Vector3(Random.Range(0f, 180f), Random.Range(0f, 180f), Random.Range(0f, 180f));
                        distance_Robot_ball = Vector3.Distance(handleRobot.transform.position, footballs[randomInt].transform.position);
                    }
                    else
                        break;
                }
                var Balldistance = Vector3.Distance(handleRobot.transform.position, footballs[randomInt].transform.position);
                randomLookAtPosition = footballs[randomInt].transform.position + new Vector3(Random.Range(-0.5f, 0.5f), 0f, Random.Range(-0.5f, 0.5f)) * (Balldistance / 2.3f);
            }
            lookAtTarget.transform.position = randomLookAtPosition;
            cameraPack.transform.LookAt(lookAtTarget.transform);
            handleRobot.transform.eulerAngles = new Vector3(0f,cameraPack.transform.eulerAngles.y,0f);
            cameraPack.transform.eulerAngles = new Vector3(cameraPack.transform.eulerAngles.x, handleRobot.transform.eulerAngles.y, 0f);

        }
        else if(nextPose == 3)
        {
            for (int i = 0; i < footballs.Count(); i++)
            {
                footballs[i].gameObject.SetActive(false);
            }
            Soccer_Ball.SetActive(true);
            var current_Robot_position = handleRobot.transform.position;
            var current_Robot_Angle = handleRobot.transform.eulerAngles;
            var next_move_point = new Vector3(0f, 0f, 0f);
            var next_lot_point = new Vector3(0f, 0f, 0f);
            if(move_mode == 8)
            {
                next_move_point = current_Robot_position + handleRobot.transform.forward*0.25f;
                next_lot_point = current_Robot_Angle;
            }
            else if (move_mode == 2)
            {
                next_move_point = current_Robot_position + handleRobot.transform.forward * -0.25f;
                next_lot_point = current_Robot_Angle;
            }
            else if (move_mode == 4)
            {
                next_move_point = current_Robot_position;
                next_lot_point = current_Robot_Angle + new Vector3(0f, -20f, 0f);
            }
            else if (move_mode == 6)
            {
                next_move_point = current_Robot_position;
                next_lot_point = current_Robot_Angle + new Vector3(0f, 20f, 0f);
            }
            else if (move_mode == 10)
            {
                next_move_point = new Vector3(Random.Range(-6f, 6f), 0.5f, Random.Range(-11f, 11f));
                next_lot_point = new Vector3(0f, Random.Range(0f, 360f), 0f);
                Soccer_Ball.transform.position = new Vector3(Random.Range(-6f, 6f), 0.5f, Random.Range(-11f, 11f));
                Soccer_Ball.transform.eulerAngles = new Vector3(Random.Range(0f, 180f), Random.Range(0f, 180f), Random.Range(0f, 180f));
            }
            else
            {
                next_move_point = current_Robot_position;
                next_lot_point = current_Robot_Angle;
            }
            handleRobot.transform.position = Vector3.MoveTowards(handleRobot.transform.position, next_move_point, 0.1f);
            handleRobot.transform.eulerAngles = Vector3.MoveTowards(handleRobot.transform.eulerAngles, next_lot_point, 1f);
            cameraPack.transform.eulerAngles = new Vector3(head_vertical * 1f, head_horizen * 1f, 0f)+handleRobot.transform.eulerAngles;
        }

    }

    public override void OnEpisodeBegin()
    {
        footballs.Clear();
        footballs.Add(football_basic);
        footballs.Add(football_red);
        footballs.Add(football_blue);
        footballs.Add(football_green);
        footballs.Add(football_white);
        footballs.Add(football_marble);
        footballs.Add(ball_red);
        footballs.Add(ball_blue);
        footballs.Add(ball_sp1);
        footballs.Add(ball_sp2);
        footballs.Add(ball_sp3);

        var randomInt = Random.Range(0, footballs.Count());
        Soccer_Ball.SetActive(false);
        for (int i = 0; i < footballs.Count(); i++)
        {
            if (i != randomInt)
                footballs[i].gameObject.SetActive(false);
            else
                footballs[i].gameObject.SetActive(true);
        }
        handleRobot.transform.position = new Vector3(0f, 2f, -7f);
        cameraPack.transform.eulerAngles = new Vector3(0f, 0f, 0f);
        footballs[randomInt].transform.position = new Vector3(0f, 0.5f, 0f);
        footballs[randomInt].transform.eulerAngles = new Vector3(Random.Range(0f, 180f), Random.Range(0f, 180f), Random.Range(0f, 180f));
    }

    public override void Heuristic(in ActionBuffers actionsOut)
    {
        var DiscreteActionsout = actionsOut.DiscreteActions;
        DiscreteActionsout[0] = 0;
        DiscreteActionsout[1] = 0;
        DiscreteActionsout[2] = 0;
        DiscreteActionsout[3] = 0;
        if (Input.GetKey(KeyCode.M))
        {
            DiscreteActionsout[0] = 1;
        }
        if (Input.GetKey(KeyCode.N))
        {
            DiscreteActionsout[0] = 2;
            DiscreteActionsout[1] = 2;
        }
        if (Input.GetKey(KeyCode.W))
        {
            DiscreteActionsout[0] = 3;
            DiscreteActionsout[1] = 8;

        }
        if (Input.GetKey(KeyCode.A))
        {
            DiscreteActionsout[0] = 3;
            DiscreteActionsout[1] = 4;
        }
        if (Input.GetKey(KeyCode.S))
        {
            DiscreteActionsout[0] = 3;
            DiscreteActionsout[1] = 2;
        }
        if (Input.GetKey(KeyCode.D))
        {
            DiscreteActionsout[0] = 3;
            DiscreteActionsout[1] = 6;
        }
        if (Input.GetKey(KeyCode.Q))
        {
            DiscreteActionsout[0] = 3;
            DiscreteActionsout[2] = 60;
        }
        if (Input.GetKey(KeyCode.E))
        {
            DiscreteActionsout[0] = 3;
            DiscreteActionsout[3] = 30;
        }
    }
}