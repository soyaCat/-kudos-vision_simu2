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
    public GameObject cameraPack;
    public GameObject lookAtTarget;
    public GameObject handleRobot;

    private List<GameObject> footballs = new List<GameObject>();


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
        var nextPose = 0;
        var randomInt = Random.Range(0, footballs.Count());
        var randomLookAtPosition = new Vector3(0f, 0f, 0f);
        switch (act0)
        {
            case 1:
                nextPose = 1;
                break;
            case 0:
                nextPose = 0;
                break;
        }
        if (nextPose == 1)
        {
            for (int i = 0; i < footballs.Count(); i++)
            {
                if (i != randomInt)
                    footballs[i].gameObject.SetActive(false);
                else
                    footballs[i].gameObject.SetActive(true);
            }
            handleRobot.transform.position = new Vector3(Random.Range(-6f, 6f), 1.875f, Random.Range(-11f, 11f));
            var distance_Robot_ball = 8f;
            while(true)
            {
                if (distance_Robot_ball >= 8f)
                {
                    footballs[randomInt].transform.position = new Vector3(Random.Range(-6f, 6f), 0.5f, Random.Range(-11f, 11f));
                    distance_Robot_ball = Vector3.Distance(handleRobot.transform.position, footballs[randomInt].transform.position);
                }
                else
                    break;
            }
            var Balldistance = Vector3.Distance(handleRobot.transform.position, footballs[randomInt].transform.position);
            randomLookAtPosition = footballs[randomInt].transform.position + new Vector3(Random.Range(-1f, 1f), 0f, Random.Range(-1f, 1f))*(Balldistance/2.3f);
            lookAtTarget.transform.position = randomLookAtPosition;
            cameraPack.transform.LookAt(lookAtTarget.transform);
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
        var randomLookAtPosition = new Vector3(0f, 0f, 0f);
        for (int i = 0; i < footballs.Count(); i++)
        {
            if (i != randomInt)
                footballs[i].gameObject.SetActive(false);
            else
                footballs[i].gameObject.SetActive(true);
        }
        handleRobot.transform.position = new Vector3(Random.Range(-6f, 6f), 1.875f, Random.Range(-11f, 11f));
        footballs[randomInt].transform.position = new Vector3(Random.Range(-6f, 6f), 0.5f, Random.Range(-11f, 11f));
        randomLookAtPosition = footballs[randomInt].transform.position + new Vector3(Random.Range(-6f, 6f), 0f, Random.Range(-6f, 6f));
        lookAtTarget.transform.position = randomLookAtPosition;
        cameraPack.transform.LookAt(lookAtTarget.transform);
    }

    public override void Heuristic(in ActionBuffers actionsOut)
    {
        var DiscreteActionsout = actionsOut.DiscreteActions;
        DiscreteActionsout[0] = 0;
        if (Input.GetKey(KeyCode.N))
        {
            DiscreteActionsout[0] = 1;
        }
    }
}