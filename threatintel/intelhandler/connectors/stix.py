from intelhandler.models import Feed, Indicator
from stix2elevator import elevate
from stix2elevator.options import initialize_options
from pprint import pprint
import uuid
import json

bundle = """
{
  "type": "bundle",
  "id": "bundle--ac946f1d-6a0e-4a9d-bc83-3f1f3bfda6ba",
  "objects": [
    {
      "type": "malware",
      "is_family": true,
      "spec_version": "2.1",
      "id": "malware--591f0cb7-d66f-4e14-a8e6-5927b597f920",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "Poison Ivy",
      "description": "Poison Ivy is a remote access tool, first released in 2005 but unchanged since 2008. It includes features common to most Windows-based RATs, including key logging, screen capturing, video capturing, file transfers, system administration, password theft, and traffic relaying.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "identity",
      "spec_version": "2.1",
      "id": "identity--81cade27-7df8-4730-836b-62d880e6d9d3",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "FireEye, Inc.",
      "identity_class": "organization",
      "sectors": [
        "technology"
      ]
    },
    {
      "type": "campaign",
      "spec_version": "2.1",
      "id": "campaign--752c225d-d6f6-4456-9130-d9580fd4007b",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "admin@338",
      "description": "Active since 2008, this campaign mostly targets the financial services industry, though we have also seen activity in the telecom, government, and defense sectors.",
      "first_seen": "2008-01-07T00:00:00.000000Z"
    },
    {
      "type": "campaign",
      "spec_version": "2.1",
      "id": "campaign--d02a1560-ff69-49f4-ac34-919b8aa4b91e",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "th3bug",
      "description": "This ongoing campaign targets a number of industries but appears to prefer targets in higher education and the healthcare sectors.",
      "first_seen": "2009-10-26T00:00:00.000000Z"
    },
    {
      "type": "campaign",
      "spec_version": "2.1",
      "id": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "menuPass",
      "description": "The threat actor behind menuPass prefers to target U.S. and foreign defense contractors.",
      "first_seen": "2009-12-14T00:00:00.000000Z"
    },
    {
      "type": "attack-pattern",
      "spec_version": "2.1",
      "id": "attack-pattern--19da6e1c-69a8-4c2f-886d-d620d09d3b5a",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "external_references": [
        {
          "source_name": "capec",
          "description": "spear phishing",
          "external_id": "CAPEC-163"
        }
      ],
      "name": "Spear Phishing Attack Pattern used by admin@338",
      "description": "The preferred attack vector used by admin@338 is spear-phishing emails. Using content that is relevant to the target, these emails are designed to entice the target to open an attachment that contains the malicious PIVY server code.",
      "kill_chain_phases": [
        {
          "kill_chain_name": "mandiant-attack-lifecycle-model",
          "phase_name": "initial-compromise"
        }
      ]
    },
    {
      "type": "attack-pattern",
      "spec_version": "2.1",
      "id": "attack-pattern--ea2c747d-4aa3-4573-8853-37b7159bc180",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "Strategic Web Compromise Attack Pattern used by th3bug",
      "description": "Attacks attributed to th3bug use a strategic Web compromise to infect targets. This approach is more indiscriminate, which probably accounts for the more disparate range of targets.",
      "kill_chain_phases": [
        {
          "kill_chain_name": "mandiant-attack-lifecycle-model",
          "phase_name": "initial-compromise"
        }
      ]
    },
    {
      "type": "attack-pattern",
      "spec_version": "2.1",
      "id": "attack-pattern--fb6aa549-c94a-4e45-b4fd-7e32602dad85",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "external_references": [
        {
          "source_name": "capec",
          "description": "spear phishing",
          "external_id": "CAPEC-163"
        }
      ],
      "name": "Spear Phishing Attack Pattern used by menuPass",
      "description": "menuPass appears to favor spear phishing to deliver payloads to the intended targets. While the attackers behind menuPass have used other RATs in their campaign, it appears that they use PIVY as their primary persistence mechanism.",
      "kill_chain_phases": [
        {
          "kill_chain_name": "mandiant-attack-lifecycle-model",
          "phase_name": "initial-compromise"
        }
      ]
    },
    {
      "type": "course-of-action",
      "spec_version": "2.1",
      "id": "course-of-action--70b3d5f6-374b-4488-8688-729b6eedac5b",
      "created_by_ref": "identity--81cade27-7df8-4730-836b-62d880e6d9d3",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "Analyze with FireEye Calamine Toolset",
      "description": "Calamine is a set of free tools to help organizations detect and examine Poison Ivy infections on their systems. The package includes these components: PIVY callback-decoding tool (ChopShop Module) and PIVY memory-decoding tool (PIVY PyCommand Script).",
      "external_references": [
        {
          "source_name": "Calamine ChopShop Module",
          "description": "The FireEye Poison Ivy decoder checks the beginning of each TCP session for possible PIVY challengeresponse sequences. If found, the module will try to validate the response using one or more passwords supplied as arguments.",
          "url": "https://github.com/fireeye/chopshop"
        },
        {
          "source_name": "Calamine PyCommand Script",
          "description": "Helps locate the PIVY password.",
          "url": "https://github.com/fireeye/pycommands"
        }
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--61a62a6a-9a18-4758-8e52-622431c4b8ae",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (808e21d6efa2884811fbd0adf67fda78)",
      "description": "The key@123 sample (password for admin@338), 808e21d6efa2884811fbd0adf67fda78, connects directly to 219.76.208.163",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--30ea087f-7d2b-496b-9ed1-5f000c8b7695",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (8010cae3e8431bb11ed6dc9acabb93b7,)",
      "description": "Two CnC domain names from the admin@338 sample 8010cae3e8431bb11ed6dc9acabb93b7, connect to www.webserver.dynssl.com and www.webserver.freetcp.com and resolve to 219.76.208.163. It also connects to the CnC domain www.webserver.fartit.com.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--4de25c38-5826-4ee7-b84d-878064de87ad",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (0323de551aa10ca6221368c4a73732e6,)",
      "description": "The gwx@123 sample 0323de551aa10ca6221368c4a73732e6 connects to the CnC domain names microsofta.byinter.net, microsoftb.byinter.net, microsoftc.byinter. net, and microsofte.byinter.net.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--dc669921-4a1a-470d-bfae-694e740ce181",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (8002debc47e04d534b45f7bb7dfcab4d)",
      "description": "The sample 8002debc47e04d534b45f7bb7dfcab4d connected to kr.iphone.qpoe.com with the PIVY password admin.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "is_family": false,
      "spec_version": "2.1",
      "id": "malware--f86febd3-609b-4d2e-9fec-aa805cb498bf",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (55a3b2656ceac2ba6257b6e39f4a5b5a)",
      "description": "The sample 55a3b2656ceac2ba6257b6e39f4a5b5a connected to ct.toh.info domain with the PIVY password th3bug.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--80c260d9-a075-4148-9301-ebe4af27f449",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (b08694e14a9b966d8033b42b58ab727d)",
      "description": "This sample (b08694e14a9b966d8033b42b58ab727d) for menuPass connected to a control server at js001.3322.org with a password xiaoxiaohuli (Chinese translation: 'little little fox')",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--3ed0364f-62c8-4ebc-b136-deaf6966880b",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (d8c00fed6625e5f8d0b8188a5caac115)",
      "description": "The sample d8c00fed6625e5f8d0b8188a5caac115 connected to apple.cmdnetview.com with the password XGstone.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--17099f03-5ec8-456d-a2de-968aebaafc78",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (b1deff736b6d12b8d98b485e20d318ea)",
      "description": "The sample b1deff736b6d12b8d98b485e20d318ea connected to autuo.xicp.net with the password keaidestone.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--e14b6476-40b5-4b0b-bde7-0e856ab00b6c",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (08709f35581e0958d1ca4e50b7d86dba)",
      "description": "The sample 08709f35581e0958d1ca4e50b7d86dba has a compile time of July 20. 2012 and connected to tw.2012yearleft.com with the password keaidestone. This sample also used the CBricksDoc launcher.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--feaf146d-ea67-4eb1-946a-6f352ff79a81",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (e84853c0484b02b7518dd683787d04f)",
      "description": "The sample e84853c0484b02b7518dd6837 87d04fc connected to dedydns.ns01.us with the password smallfish and used the CBricksDoc launcher.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--13791e02-6621-45fb-8c10-f6b72e1bf553",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (cf8094c07c15aa394dddd4eca4aa8c8b)",
      "description": "The sample cf8094c07c15aa394dddd4eca4aa8c8b connected to maofajapa.3322.org with the password happyyongzi.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--703a15a7-eb85-475d-a27a-77d8fcf8f7b9",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (410eeaa18dbec01a27c5b41753b3c7ed )",
      "description": "The sample 410eeaa18dbec01a27c5b41753b3c7ed connected to send.have8000.com with the password of suzuki.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--fade08cb-fa57-485e-97f8-fab5a1bd4460",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (b2dc98caa647e64a2a8105c298218462)",
      "description": "The sample b2dc98caa647e64a2a8105c298218462 connected to apple.cmdnetview.com with the password XGstone.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--3050937d-6330-44c7-83ba-8821e1f7e7bd",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (68fec995a13762184a2616bda86757f8)",
      "description": "68fec995a13762184a2616bda86757f8 had a compile time of March 25, 2012 and connected to fbi.zyns.com with the password menuPass. This sample also used the CBricksDoc launcher.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--9d995717-edc3-4bd8-8554-aecf773bdecc",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (39a59411e7b12236c0b4351168fb47ce)",
      "description": "The sample 39a59411e7b12236c0b4351168fb47ce had a compile time of April 2, 2010 and connected to weile3322b.3322.org with the password keaidestone. This sample used a launcher of CPiShellPutDoc.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--40e15fa5-df8d-4771-a682-21dab0a024fd",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (f5315fb4a654087d30c69c768d80f826)",
      "description": "The sample f5315fb4a654087d30c69c768d80f826 had a compile time of May 21, 2010 and connected to ngcc.8800.org with the password menuPass. This sample also used a launcher of CPiShellPutDoc.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--69101c2f-da92-47af-b402-7c60a39a982f",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (e6ca06e9b000933567a8604300094a85)",
      "description": "The sample e6ca06e9b000933567a8604300094a85 connected to the domain sh.chromeenter.com with the password happyyongzi.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--1601b8c2-5e6f-4a18-a413-10527e5d90b7",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (56cff0d0e0ce486aa0b9e4bc0bf2a141)",
      "description": "The sample 56cff0d0e0ce486aa0b9e4bc0bf2a141 was compiled on 2011-08-31 and connected to mf.ddns.info with the password menuPass.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--626badcc-4257-4222-946c-6d6e889836ea",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (60963553335fa5877bd5f9be9d8b23a6 )",
      "description": "The sample 60963553335fa5877bd5f9be9d8b23a6 was compiled on June 9, 2012 and connected to av.ddns.us with the password of admin",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--3b275ed1-9c2e-4443-b1dd-5cfb51eaef2e",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (6d989302166ba1709d66f90066c2fd59)",
      "description": "A number of menuPass and admin samples also shared the same CBricksDoc launcher including but not limited to 6d989302166ba1709d66f90066c2fd59.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--f138b6e0-9a7d-4cd9-a904-08a7df2eabb1",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (4bc6cab128f623f34bb97194da21d7b6)",
      "description": "A number of menuPass and admin samples also shared the same CBricksDoc launcher including but not limited to 4bc6cab128f623f34bb97194da21d7b6.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--302ac5b5-486c-4c99-8cad-4426aeaf47b6",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (4e84b1448cf96fabe88c623b222057c4)",
      "description": "The sample 4e84b1448cf96fabe88c623b222057c4 connected to jj.mysecondarydns.com with the password menuPass",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--e1c02dca-d3fe-48f1-bb4b-3cacd2bc3619",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (494e65cf21ad559fccf3dacdd69acc94)",
      "description": "The sample 494e65cf21ad559fccf3dacdd69acc94 connected to mongoles.3322.org with the password fishplay. It also connects to CBricksDoc.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "malware",
      "spec_version": "2.1",
      "is_family": true,
      "id": "malware--a4f315bd-e159-4bfb-8439-0d5a8330fc70",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "PIVY Variant (a5965b750997dbecec61358d41ac93c7)",
      "description": "The sample a5965b750997dbecec61358d41ac93c7 connected to 3q.wubangtu.info with the password menuPass. It also connects to CBricksDoc.",
      "malware_types": [
        "remote-access-trojan"
      ]
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--e8094b09-7df4-4b13-b207-1e27af3c4bde",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "IP address: 219.76.208.163",
      "description": "IP address for key@123 sample 808e21d6efa2884811fbd0adf67fda78",
      "pattern": "[ipv4-addr:value = '219.76.208.163']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--329ae6e9-25bd-49e8-89d1-aae4ca52e4a7",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "www.webserver.dynssl.com",
      "description": "www.webserver.dynssl.com resolved to 113.10.246.30, 219.90.112.203, 219.90.112.203, 75.126.95.138, 219.90.112.197, and 202.65.222.45, which overlap with the gwx@123 IP addresses.",
      "pattern": "[domain-name:value = 'www.webserver.dynssl.com' OR ipv4-addr:value = '113.10.246.30' OR ipv4-addr:value = '219.90.112.203' OR ipv4-addr:value = '75.126.95.138' OR ipv4-addr:value = '219.90.112.197' OR ipv4-addr:value = '202.65.222.45']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--54e1e351-fec0-41a4-b62c-d7f86101e241",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "www.webserver.freetcp.com",
      "description": "www.webserver.freetcp.com resolved to 113.10.246.30, 219.90.112.203, 202.65.220.64, 75.126.95.138, 219.90.112.197, and 202.65.222.45, which overlap with the gwx@123 IP addresses.",
      "pattern": "[domain-name:value = 'www.webserver.freetcp.com' OR ipv4-addr:value = '113.10.246.30' OR ipv4-addr:value = '219.90.112.203' OR ipv4-addr:value = '202.65.220.64' OR ipv4-addr:value = '75.126.95.138' OR ipv4-addr:value = '219.90.112.197' OR ipv4-addr:value = '202.65.222.45']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--2e59f00b-0986-437e-9ebd-e0d61900d688",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "www.webserver.fartit.com",
      "description": "www.webserver.fartit.com resolved to 113.10.246.30, 219.90.112.203, 202.65.220.64, and 75.126.95.138, which overlap with the gwx@123 IP addresses.",
      "pattern": "[domain-name:value = 'www.webserver.fartit.com' OR ipv4-addr:value = '113.10.246.30' OR ipv4-addr:value = '219.90.112.203' OR ipv4-addr:value = '202.65.220.64' OR ipv4-addr:value = '75.126.95.138']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--8da68996-f175-4ae0-bd74-aad4913873b8",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "microsoft.byinter.net",
      "description": "The gwx@123 sample 0323de551aa10ca6221368c4a73732e6 connects to the CnC domain names microsofta.byinter.net, microsoftb.byinter.net, microsoftc.byinter.net, and microsofte.byinter.net. These domain names resolved to 113.10.246.30, 219.90.112.203, 202.65.220.64, 75.126.95.138, 219.90.112.197, 202.65.222.45, and 98.126.148.114.",
      "pattern": "[domain-name:value = 'microsofta.byinter.net' OR domain-name:value = 'microsoftb.byinter.net' OR domain-name:value = 'microsoftc.byinter.net' OR domain-name:value = 'microsofte.byinter.net' OR ipv4-addr:value = '113.10.246.30' OR ipv4-addr:value = '219.90.112.203' OR ipv4-addr:value = '202.65.220.64' OR ipv4-addr:value = '75.126.95.138' OR ipv4-addr:value = '219.90.112.197' OR ipv4-addr:value = '202.65.222.45' OR ipv4-addr:value = '98.126.148.114']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--4e11b23f-732b-418e-b786-4dbf65459d50",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "nkr.iphone.qpoe.com",
      "description": "th3bug used domain name: nkr.iphone.qpoe.com. The domain nkr.iphone.qpoe.com resolved to 180.210.206.96 on January 12, 2012 and also 101.78.151.179 on December 23, 2011.",
      "pattern": "[domain-name:value = 'nkr.iphone.qpoe.com' OR ipv4-addr:value = '180.210.206.96' OR ipv4-addr:value = '101.78.151.179']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--b7fa7e73-e645-4813-9723-161bbd8dda62",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "e.ct.toh.info",
      "description": "th3bug used domain name: e.ct.toh.info. The domain e.ct.toh.info resolved to 101.78.151.179 on June 12, 2012. The sample 55a3b2656ceac2ba6257b6e39f4a5b5a connected to ct.toh.info domain with the PIVY password th3bug.",
      "pattern": "[domain-name:value = 'e.ct.toh.info' OR ipv4-addr:value = '101.78.151.179']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--b2f09ce0-2db4-480f-bd2f-073ddb3a0c87",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "js001.3322.org",
      "description": "menuPass used control server: js001.3322.org. The sample (b08694e14a9b966d8033b42b58ab727d) connected to a control server at js001.3322.org with a password xiaoxiaohuli (Chinese translation: 'little little fox')",
      "pattern": "[domain-name:value = 'js001.3322.org' OR ipv4-addr:value = '101.78.151.179']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--9842a3b9-fc5b-44c4-bb48-578cf6f728d9",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "apple.cmdnetview.com",
      "description": "menuPass used domain: apple.cmdnetview.com. The sample d8c00fed6625e5f8d0b8188a5caac115 connected to apple.cmdnetview.com with the password XGstone. IP 60.10.1.120 hosted this domain.",
      "pattern": "[domain-name:value = 'apple.cmdnetview.com' OR ipv4-addr:value = '60.10.1.120']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--4e4c4ad7-4909-456a-b6fa-e24a6f682a40",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "autuo.xicp.net",
      "description": "menuPass used domain: autuo.xicp.net. The sample b1deff736b6d12b8d98b485e20d318ea connected to autuo.xicp.net with the password keaidestone. IP 60.10.1.115 hosted this domain.",
      "pattern": "[domain-name:value = 'domain autuo.xicp.net' OR ipv4-addr:value = '60.10.1.115']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--137acf67-cedc-4a07-8719-72759174de3a",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "CBricksDoc",
      "description": "menuPass uses Microsoft Foundation Class Library class name CBricksDoc as a launcher for PIVY.",
      "pattern": "[file:name = 'CBricksDoc']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--9695dc2f-d92a-4f2b-8b16-b0e21d7c631d",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "tw.2012yearleft.com",
      "description": "08709f35581e0958d1ca4e50b7d86dba has a compile time of July 20. 2012 and connected to tw.2012yearleft.com with the password keaidestone. 2012yearleft.com was registered on February 13, 2012 by zhengyanbin8@gmail.com.",
      "pattern": "[domain-name:value = 'tw.2012yearleft.com' OR ipv4-addr:value = '60.10.1.114' OR ipv4-addr:value = '60.1.1.114']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--7fd865ed-93e9-481f-953b-82ab386190ae",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "dedydns.ns01.us",
      "description": "The domain dedydns.ns01.us resolved to 60.10.1.121. The sample e84853c0484b02b7518dd6837 87d04fc connected to dedydns.ns01.us with the password smallfish and used the CBricksDoc launcher.",
      "pattern": "[domain-name:value = 'dedydns.ns01.us' OR ipv4-addr:value = '60.10.1.121']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--e5bc6507-d052-447f-93c7-db7ef32211da",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "maofajapa.3322.org",
      "description": "The domain maofajapa.3322.org resolved to 60.10.1.121. The sample cf8094c07c15aa394dddd4eca4aa8c8b connected to maofajapa.3322.org with the password happyyongzi.",
      "pattern": "[domain-name:value = 'maofajapa.3322.org' OR ipv4-addr:value = '60.10.1.121']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--fead5c52-9533-405c-b822-a034092a1ba8",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "send.have8000.com",
      "description": "The sample 410eeaa18dbec01a27c5b41753b3c7ed connected to send.have8000.com with the password of suzuki. The domain have8000.com was registered on 2012-02-13 via the email zhengyanbin8@ gmail.com.",
      "pattern": "[domain-name:value = 'send.have8000.com']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--405ff732-2c35-4f46-9f78-2a632ce36e03",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "fbi.zyns.com",
      "description": "The domain fbi.zyns.com resolved to 60.10.1.118 on August 21, 2012. 68fec995a13762184a2616bda86757f8 had a compile time of March 25, 2012 and connected to fbi.zyns.com with the password menuPass.",
      "pattern": "[domain-name:value = 'fbi.zyns.com' OR ipv4-addr:value = '60.10.1.118']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--4d58096e-b5c9-47d8-af9a-1af5f4762d6b",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "weile3322b.3322.org",
      "description": "The sample 39a59411e7b12236c0b4351168fb47ce had a compile time of April 2, 2010 and connected to weile3322b.3322.org with the password keaidestone.",
      "pattern": "[domain-name:value = 'weile3322b.3322.org']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--9c725598-a160-4e91-8b93-ed0956709892",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "ngcc.8800.org",
      "description": "The sample f5315fb4a654087d30c69c768d80f826 had a compile time of May 21, 2010 and connected to ngcc.8800.org with the password menuPass",
      "pattern": "[domain-name:value = 'ngcc.8800.org']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--2efe7c62-1b96-4568-81ee-c85b840bde39",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "sh.chromeenter.com",
      "description": "The sample e6ca06e9b000933567a8604300094a85 connected to the domain sh.chromeenter.com with the password happyyongzi. The domain sh.chromeenter.com previously resolved to the IP 60.2.148.167.",
      "pattern": "[domain-name:value = 'sh.chromeenter.com' OR ipv4-addr:value = '60.2.148.167']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--b8322c9b-8031-4fb3-9cbc-8a1ea0fe3cfa",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "mf.ddns.info",
      "description": "The sample 56cff0d0e0ce486aa0b9e4bc0bf2a141 was compiled on 2011-08-31 and connected to mf.ddns.info with the password menuPass. The domain mf.ddns.info resolved to 54.241.8.84 on November 22, 2012. This same IP also hosted the domain av.ddns.us on the same date.",
      "pattern": "[domain-name:value = 'mf.ddns.info' OR ipv4-addr:value = '60.2.148.167']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--b08f9631-dd94-4d99-a96c-32b42af2ea81",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "av.ddns.us",
      "description": "The sample 60963553335fa5877bd5f9be9d8b23a6 was compiled on June 9, 2012 and connected to av.ddns.us with the password of admin.",
      "pattern": "[domain-name:value = 'av.ddns.us' OR ipv4-addr:value = '60.2.148.167']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--950c01b8-c647-4cc8-b0c1-3612fa780108",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "jj.mysecondarydns.com",
      "description": "The sample 4e84b1448cf96fabe88c623b222057c4 connected to jj.mysecondarydns.com with the password menuPass. The domain jj.mysecondarydns.com also resolved to 60.2.148.167.",
      "pattern": "[domain-name:value = 'jj.mysecondarydns.com' OR ipv4-addr:value = '60.2.148.167']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--ae29faa6-5f70-4eb8-981b-30818433a52e",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "mongoles.3322.org",
      "description": "The sample 494e65cf21ad559fccf3dacdd69acc94 connected to mongoles.3322.org with the password fishplay.",
      "pattern": "[domain-name:value = 'mongoles.3322.org' OR ipv4-addr:value = '123.183.210.28']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--b6cc482d-89db-4e6b-a592-723070f6d22d",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "3q.wubangtu.info",
      "description": "The sample a5965b750997dbecec61358d41ac93c7 connected to 3q.wubangtu.info with the password menuPass. The domain wubangtu.info also resolved to 123.183.210.28.",
      "pattern": "[domain-name:value = '3q.wubangtu.info' OR ipv4-addr:value = '123.183.210.28']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "indicator",
      "spec_version": "2.1",
      "pattern_type": "stix",
      "id": "indicator--0b71628d-31dd-4eb8-baee-39f19c0a14b0",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "CPiShellPutDoc",
      "description": "menuPass uses CPiShellPutDoc as a launcher for PIVY.",
      "pattern": "[file:name = 'CPiShellPutDoc']",
      "indicator_types": [
        "malicious-activity",
        "attribution"
      ],
      "valid_from": "2015-05-15T09:12:16.432678Z"
    },
    {
      "type": "vulnerability",
      "spec_version": "2.1",
      "id": "vulnerability--c7cab3fb-0822-43a5-b1ba-c9bab34361a2",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "CVE-2012-0158",
      "description": "Weaponized Microsoft Word document used by admin@338",
      "external_references": [
        {
          "source_name": "cve",
          "external_id": "CVE-2012-0158"
        }
      ]
    },
    {
      "type": "vulnerability",
      "spec_version": "2.1",
      "id": "vulnerability--6a2eab9c-9789-4437-812b-d74323fa3bca",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "CVE-2009-4324",
      "description": "Adobe acrobat PDF's used by admin@338",
      "external_references": [
        {
          "source_name": "cve",
          "external_id": "CVE-2009-4324"
        }
      ]
    },
    {
      "type": "vulnerability",
      "spec_version": "2.1",
      "id": "vulnerability--2b7f00d8-b133-4a92-9118-46ce5f8b2531",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "CVE-2013-0422",
      "description": "Java 7 vulnerability exploited by th3bug",
      "external_references": [
        {
          "source_name": "cve",
          "external_id": "CVE-2013-0422"
        }
      ]
    },
    {
      "type": "vulnerability",
      "spec_version": "2.1",
      "id": "vulnerability--4d7dc9cb-983f-40b4-b597-d7a38b2d9a4b",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "CVE-2013-1347",
      "description": "Microsoft Internet Explorer 8 vulnerability exploited by th3bug",
      "external_references": [
        {
          "source_name": "cve",
          "external_id": "CVE-2013-1347"
        }
      ]
    },
    {
      "type": "vulnerability",
      "spec_version": "2.1",
      "id": "vulnerability--8323404c-1fdd-4272-822b-829f85556c53",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "CVE-2011-3544",
      "description": "JRE vulnerability exploited by th3bug",
      "external_references": [
        {
          "source_name": "cve",
          "external_id": "CVE-2011-3544"
        }
      ]
    },
    {
      "type": "vulnerability",
      "spec_version": "2.1",
      "id": "vulnerability--717cb1c9-eab3-4330-8340-e4858055aa80",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "CVE-2010-3333",
      "description": "menuPass campaign using weaponized Microsoft Word documents, exploiting this vulnerability",
      "external_references": [
        {
          "source_name": "cve",
          "external_id": "CVE-2010-3333"
        }
      ]
    },
    {
      "type": "report",
      "spec_version": "2.1",
      "id": "report--f2b63e80-b523-4747-a069-35c002c690db",
      "created_by_ref": "identity--81cade27-7df8-4730-836b-62d880e6d9d3",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "Poison Ivy: Assessing Damage and Extracting Intelligence",
      "report_types": [
        "threat-report",
        "malware"
      ],
      "published": "2013-08-21T00:00:00.000000Z",
      "description": "This report spotlights Poison Ivy (PIVY), a RAT that remains popular and effective a full eight years after its release, despite its age and familiarity in IT security circles. Poison Ivy is a remote access tool that is freely available for download from its official web site at www.poisonivy-rat.com. First released in 2005, the tool has gone unchanged since 2008 with version 2.3.2. Poison Ivy includes features common to most Windows-based RATs, including key logging, screen capturing, video capturing, file transfers, system administration, password theft, and traffic relaying. Poison Ivy's wide availability and easy-to-use features make it a popular choice for all kinds of criminals. But it is probably most notable for its role in many high profile, targeted APT attacks. These APTs pursue specific targets, using RATs to maintain a persistent presence within the target's network. They move laterally and escalate system privileges to extract sensitive information-whenever the attacker wants to do so. Because some RATs used in targeted attacks are widely available, determining whether an attack is part of a broader APT campaign can be difficult. Equally challenging is identifying malicious traffic to determine the attacker's post-compromise activities and assess overall damage - these RATs often encrypt their network communications after the initial exploit. In 2011, three years after the most recent release of PIVY, attackers used the RAT to compromise security firm RSA and steal data about its SecureID authentication system. That data was subsequently used in other attacks. The RSA attack was linked to Chinese threat actors and described at the time as extremely sophisticated. Exploiting a zero-day vulnerability, the attack delivered PIVY as the payload. It was not an isolated incident. The campaign appears to have started in 2010, with many other companies compromised. PIVY also played a key role in the 2011 campaign known as Nitro that targeted chemical makers, government agencies, defense contractors, and human rights groups. Still active a year later, the Nitro attackers used a zero-day vulnerability in Java to deploy PIVY in 2012. Just recently, PIVY  was the payload of a zero-day exploit in Internet Explorer used in what is known as a 'strategic web compromise' attack against visitors to a U.S. government website and a variety of others. RATs require live, direct, real-time human interaction by the APT attacker. This characteristic is distinctly different from crimeware (malware focused on cybercrime), where the criminal can issue commands to their botnet of compromised endpoints whenever they please and set them to work on a common goal such as a spam relay. In contrast, RATs are much more personal and may indicate that you are dealing with a dedicated threat actor that is interested in your organization specifically.",
      "object_refs": [
        "malware--591f0cb7-d66f-4e14-a8e6-5927b597f920",
        "malware--61a62a6a-9a18-4758-8e52-622431c4b8ae",
        "malware--30ea087f-7d2b-496b-9ed1-5f000c8b7695",
        "malware--4de25c38-5826-4ee7-b84d-878064de87ad",
        "malware--dc669921-4a1a-470d-bfae-694e740ce181",
        "malware--f86febd3-609b-4d2e-9fec-aa805cb498bf",
        "malware--80c260d9-a075-4148-9301-ebe4af27f449",
        "malware--3ed0364f-62c8-4ebc-b136-deaf6966880b",
        "malware--17099f03-5ec8-456d-a2de-968aebaafc78",
        "malware--feaf146d-ea67-4eb1-946a-6f352ff79a81",
        "malware--13791e02-6621-45fb-8c10-f6b72e1bf553",
        "malware--703a15a7-eb85-475d-a27a-77d8fcf8f7b9",
        "malware--fade08cb-fa57-485e-97f8-fab5a1bd4460",
        "malware--3050937d-6330-44c7-83ba-8821e1f7e7bd",
        "malware--9d995717-edc3-4bd8-8554-aecf773bdecc",
        "malware--40e15fa5-df8d-4771-a682-21dab0a024fd",
        "malware--69101c2f-da92-47af-b402-7c60a39a982f",
        "malware--1601b8c2-5e6f-4a18-a413-10527e5d90b7",
        "malware--626badcc-4257-4222-946c-6d6e889836ea",
        "malware--3b275ed1-9c2e-4443-b1dd-5cfb51eaef2e",
        "malware--f138b6e0-9a7d-4cd9-a904-08a7df2eabb1",
        "malware--302ac5b5-486c-4c99-8cad-4426aeaf47b6",
        "malware--e1c02dca-d3fe-48f1-bb4b-3cacd2bc3619",
        "malware--a4f315bd-e159-4bfb-8439-0d5a8330fc70",
        "identity--81cade27-7df8-4730-836b-62d880e6d9d3",
        "campaign--752c225d-d6f6-4456-9130-d9580fd4007b",
        "campaign--d02a1560-ff69-49f4-ac34-919b8aa4b91e",
        "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
        "attack-pattern--19da6e1c-69a8-4c2f-886d-d620d09d3b5a",
        "attack-pattern--ea2c747d-4aa3-4573-8853-37b7159bc180",
        "attack-pattern--fb6aa549-c94a-4e45-b4fd-7e32602dad85",
        "course-of-action--70b3d5f6-374b-4488-8688-729b6eedac5b",
        "indicator--e8094b09-7df4-4b13-b207-1e27af3c4bde",
        "indicator--329ae6e9-25bd-49e8-89d1-aae4ca52e4a7",
        "indicator--54e1e351-fec0-41a4-b62c-d7f86101e241",
        "indicator--2e59f00b-0986-437e-9ebd-e0d61900d688",
        "indicator--8da68996-f175-4ae0-bd74-aad4913873b8",
        "indicator--4e11b23f-732b-418e-b786-4dbf65459d50",
        "indicator--b7fa7e73-e645-4813-9723-161bbd8dda62",
        "indicator--b2f09ce0-2db4-480f-bd2f-073ddb3a0c87",
        "indicator--9842a3b9-fc5b-44c4-bb48-578cf6f728d9",
        "indicator--4e4c4ad7-4909-456a-b6fa-e24a6f682a40",
        "indicator--137acf67-cedc-4a07-8719-72759174de3a",
        "indicator--9695dc2f-d92a-4f2b-8b16-b0e21d7c631d",
        "indicator--7fd865ed-93e9-481f-953b-82ab386190ae",
        "indicator--e5bc6507-d052-447f-93c7-db7ef32211da",
        "indicator--fead5c52-9533-405c-b822-a034092a1ba8",
        "indicator--405ff732-2c35-4f46-9f78-2a632ce36e03",
        "indicator--4d58096e-b5c9-47d8-af9a-1af5f4762d6b",
        "indicator--9c725598-a160-4e91-8b93-ed0956709892",
        "indicator--2efe7c62-1b96-4568-81ee-c85b840bde39",
        "indicator--b8322c9b-8031-4fb3-9cbc-8a1ea0fe3cfa",
        "indicator--b08f9631-dd94-4d99-a96c-32b42af2ea81",
        "indicator--950c01b8-c647-4cc8-b0c1-3612fa780108",
        "indicator--ae29faa6-5f70-4eb8-981b-30818433a52e",
        "indicator--b6cc482d-89db-4e6b-a592-723070f6d22d",
        "indicator--0b71628d-31dd-4eb8-baee-39f19c0a14b0",
        "vulnerability--c7cab3fb-0822-43a5-b1ba-c9bab34361a2",
        "vulnerability--6a2eab9c-9789-4437-812b-d74323fa3bca",
        "vulnerability--2b7f00d8-b133-4a92-9118-46ce5f8b2531",
        "vulnerability--4d7dc9cb-983f-40b4-b597-d7a38b2d9a4b",
        "vulnerability--8323404c-1fdd-4272-822b-829f85556c53",
        "vulnerability--717cb1c9-eab3-4330-8340-e4858055aa80",
        "relationship--26c5311c-9d9b-4b9b-b3b5-bac10e16a7a3",
        "relationship--e794befc-3270-4050-b560-b6b080ab0418",
        "relationship--77a4c40e-3c33-43dc-8c78-04992ebcabf2",
        "relationship--a91f3d5c-ceac-44cf-b92b-efb819241606",
        "relationship--134c393e-cbe0-433c-9a7a-95263ed8578f",
        "relationship--900b11dc-bfa7-4dea-adb6-0e8d726b4ded",
        "relationship--8076ec7c-f6f6-4dca-a239-8bb6b5ad0c10",
        "relationship--0dd66a71-c45b-4786-bd7b-92cf952afdc1",
        "relationship--dc37f2bb-1a45-48b1-864e-c34dcde75d1d",
        "relationship--670ae011-1649-44e2-a63e-ead0b4a4cffd",
        "relationship--1a2a3630-5764-4d6e-a3c3-cb4ca27ff5f5",
        "relationship--b5046891-d2c0-4497-a167-594f778517f8",
        "relationship--253dbb93-c6f9-4839-8ce9-026c7b0a81e1",
        "relationship--d70ebcc3-5640-423d-b9b0-7158c532c040",
        "relationship--3bb540a4-c3be-478e-85e2-2a6c294c3dbd",
        "relationship--4e726ced-0207-4196-8a14-4400c09b039e",
        "relationship--b9736cd3-9482-4094-9178-1cde2b273aff",
        "relationship--70205e3e-195d-4bd5-a208-ada6cdf143e3",
        "relationship--6bb5a995-b874-4e17-88eb-38e00c8e5740",
        "relationship--d4247377-5302-4ede-a0f2-579f7db67bb6",
        "relationship--b8617e55-00c0-4066-8222-927846edcafe",
        "relationship--f34d9e2e-715f-4baf-8226-40abfcb91012",
        "relationship--937f310a-396a-403f-bb6f-400ad8920018",
        "relationship--14a06709-3c0b-4e72-ad49-dd0f6d775e65",
        "relationship--5f6c6509-ca0c-43db-8c0e-8e138f6d913c",
        "relationship--ca99fa83-0d1b-4ddd-88c8-0dee38856a88",
        "relationship--38a52125-130f-4ce7-9b38-f234553ba83d",
        "relationship--e13b17d0-1fef-4f98-a4a8-895c3e4cf1e2",
        "relationship--262a8234-d7e2-477a-baeb-ed65b639e33a",
        "relationship--f4ceabc6-9302-4dc5-9cc1-4d40ef43503c",
        "relationship--56b1023c-9e28-4449-8b4f-bc2adde45e1a",
        "relationship--8997440e-00f5-48e1-8b56-69d3b6f9f1fd",
        "relationship--80ac0601-0660-4057-b3b0-dca0fe35a6b4",
        "relationship--2583921a-2f02-42c5-bd25-0f37eb2e6ef9",
        "relationship--7231e729-42e3-4f29-ae6f-6d80192c4bd1",
        "relationship--201ee2d5-74f4-4beb-b13a-34d948854655",
        "relationship--afee4dc4-7d0e-450d-9164-4429649ab386",
        "relationship--ed403d0d-b55d-4e78-94d3-4e035a045c39",
        "relationship--4303ebf2-9590-4ec0-a702-e7bfff64bc5f",
        "relationship--54f845bb-0967-4c0f-ac8a-8ad4785cbbe6",
        "relationship--0bd19ca0-2bbb-4df0-92ec-59a4e9169c64",
        "relationship--89ddeb74-ea26-44f9-bb6d-3f17c9d4efaa",
        "relationship--eb400750-c866-47c3-89a2-fa6d1a90e9e7",
        "relationship--7450856e-051f-4d49-953c-ad24f170af0e",
        "relationship--1d6b0425-603d-4217-948a-fabb2a398450",
        "relationship--1895dd86-dc46-4505-ba62-5724a1df2362",
        "relationship--a4e0751d-8d59-4447-96ea-3799fecf66d7",
        "relationship--258796f6-e46a-421a-b3f5-7db6114fb2bc",
        "relationship--9431d9f9-6d8b-4373-b42c-172a663391b3",
        "relationship--07d2f213-1794-483e-b95b-03761826c052",
        "relationship--aa430e5b-0519-4e94-bc2c-8836d196acd7",
        "relationship--c0786bd4-9c15-48ee-a19e-a9d6aba25d67",
        "relationship--498b9f3b-488b-40d5-aaaf-e67b93c1d92b",
        "relationship--d875538e-cc47-4353-a572-2dae27ef0a44",
        "relationship--313d56c4-eef9-417e-952d-073690c20ee4",
        "relationship--6b091c0f-a700-4f3e-9d98-0b8abf9a306b",
        "relationship--5aff864a-1789-4df2-87fa-03ec43cf4fdd",
        "relationship--325ebcb6-723c-4f50-8a32-aca18809e6eb",
        "relationship--0cb9c725-3d55-4165-b2a9-9414d7933987",
        "relationship--640a0454-57eb-408f-aa13-b5732b4d0b6f",
        "relationship--41550302-6e95-4cf6-8d7c-d417a99d98dc",
        "relationship--911dcbb0-96f4-4995-9961-5ea4b2fa7ce2",
        "relationship--7b6ba584-fa87-4a6f-8c21-8123fa88db74",
        "relationship--69101c2f-da92-47af-b402-7c60a39a982f",
        "relationship--25055108-a2ae-4855-bd5f-6ab396aacbc5",
        "relationship--44c80cab-73ce-4b17-a4cb-9a36e2585403",
        "relationship--32655cb3-7455-4761-b1f2-0b82153a0540",
        "relationship--fe963c8c-65a4-49ea-910b-e1cf3c80f1b4",
        "relationship--4b0abf75-6f05-4bd5-8ac5-19778b245274",
        "relationship--154049a5-731d-4e50-af13-f0f2c9b71f91",
        "relationship--db55db06-499d-4867-9ab9-3ed4331eedb2",
        "relationship--cc802697-7677-4bd7-a8b9-e728788ac783",
        "relationship--a371be18-8ca5-4453-80f5-ae52d982c21b",
        "relationship--9a3bd620-01b5-4764-beb0-f085417ed8f3",
        "relationship--48906405-9980-4583-8559-2085c111bf89",
        "relationship--13222c71-d8fa-4688-adae-c3f8ca43a41b",
        "relationship--73c4529e-560e-4831-8497-a0db72f7dfd8",
        "relationship--8d3e1ed6-7d9c-4aa5-b121-f4eb193312cf",
        "relationship--2c11dcc0-7968-4c07-bdde-791a8f5e2e37",
        "relationship--fd97d0ef-370e-4b6f-b2d3-8fb881aadc3f",
        "relationship--c05d2410-848c-47e5-a94f-c64510e2b08d",
        "relationship--92a21b52-2961-42aa-8b01-54ea294d9d73",
        "relationship--76a9283a-b844-47a5-a5d0-b31859115f88",
        "relationship--bbd3ba5c-2a75-4902-bd42-1215a2bc320e",
        "relationship--4f784f2f-7d8e-4f12-9ddd-b685055f8076",
        "relationship--263e38f4-8ecb-414f-b3c4-0f045d1be5ed",
        "relationship--a56e8582-fc6e-4be8-bf35-7e939269d65e",
        "relationship--d7d9952c-4443-4711-a48c-7009a0f0f8ea",
        "relationship--78f110e6-2cd6-442e-971f-a2ff40c3b843",
        "relationship--b2fb88f2-5ad7-4c07-b4b2-61986decb477"
      ]
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--26c5311c-9d9b-4b9b-b3b5-bac10e16a7a3",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--752c225d-d6f6-4456-9130-d9580fd4007b",
      "target_ref": "attack-pattern--19da6e1c-69a8-4c2f-886d-d620d09d3b5a"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--e794befc-3270-4050-b560-b6b080ab0418",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--d02a1560-ff69-49f4-ac34-919b8aa4b91e",
      "target_ref": "attack-pattern--ea2c747d-4aa3-4573-8853-37b7159bc180"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--77a4c40e-3c33-43dc-8c78-04992ebcabf2",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "attack-pattern--fb6aa549-c94a-4e45-b4fd-7e32602dad85"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--134c393e-cbe0-433c-9a7a-95263ed8578f",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "mitigates",
      "source_ref": "course-of-action--70b3d5f6-374b-4488-8688-729b6eedac5b",
      "target_ref": "malware--591f0cb7-d66f-4e14-a8e6-5927b597f920"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--a91f3d5c-ceac-44cf-b92b-efb819241606",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--752c225d-d6f6-4456-9130-d9580fd4007b",
      "target_ref": "malware--61a62a6a-9a18-4758-8e52-622431c4b8ae"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--900b11dc-bfa7-4dea-adb6-0e8d726b4ded",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--e8094b09-7df4-4b13-b207-1e27af3c4bde",
      "target_ref": "malware--61a62a6a-9a18-4758-8e52-622431c4b8ae"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--8076ec7c-f6f6-4dca-a239-8bb6b5ad0c10",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--e8094b09-7df4-4b13-b207-1e27af3c4bde",
      "target_ref": "campaign--752c225d-d6f6-4456-9130-d9580fd4007b"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--0dd66a71-c45b-4786-bd7b-92cf952afdc1",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--329ae6e9-25bd-49e8-89d1-aae4ca52e4a7",
      "target_ref": "campaign--752c225d-d6f6-4456-9130-d9580fd4007b"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--dc37f2bb-1a45-48b1-864e-c34dcde75d1d",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--329ae6e9-25bd-49e8-89d1-aae4ca52e4a7",
      "target_ref": "malware--30ea087f-7d2b-496b-9ed1-5f000c8b7695"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--670ae011-1649-44e2-a63e-ead0b4a4cffd",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--8da68996-f175-4ae0-bd74-aad4913873b8",
      "target_ref": "campaign--752c225d-d6f6-4456-9130-d9580fd4007b"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--1a2a3630-5764-4d6e-a3c3-cb4ca27ff5f5",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--8da68996-f175-4ae0-bd74-aad4913873b8",
      "target_ref": "malware--4de25c38-5826-4ee7-b84d-878064de87ad"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--b5046891-d2c0-4497-a167-594f778517f8",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--2e59f00b-0986-437e-9ebd-e0d61900d688",
      "target_ref": "campaign--752c225d-d6f6-4456-9130-d9580fd4007b"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--253dbb93-c6f9-4839-8ce9-026c7b0a81e1",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--2e59f00b-0986-437e-9ebd-e0d61900d688",
      "target_ref": "malware--30ea087f-7d2b-496b-9ed1-5f000c8b7695"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--d70ebcc3-5640-423d-b9b0-7158c532c040",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "targets",
      "source_ref": "campaign--752c225d-d6f6-4456-9130-d9580fd4007b",
      "target_ref": "vulnerability--c7cab3fb-0822-43a5-b1ba-c9bab34361a2"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--3bb540a4-c3be-478e-85e2-2a6c294c3dbd",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "targets",
      "source_ref": "campaign--752c225d-d6f6-4456-9130-d9580fd4007b",
      "target_ref": "vulnerability--6a2eab9c-9789-4437-812b-d74323fa3bca"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--4e726ced-0207-4196-8a14-4400c09b039e",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "targets",
      "source_ref": "attack-pattern--19da6e1c-69a8-4c2f-886d-d620d09d3b5a",
      "target_ref": "vulnerability--c7cab3fb-0822-43a5-b1ba-c9bab34361a2"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--b9736cd3-9482-4094-9178-1cde2b273aff",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "targets",
      "source_ref": "attack-pattern--19da6e1c-69a8-4c2f-886d-d620d09d3b5a",
      "target_ref": "vulnerability--6a2eab9c-9789-4437-812b-d74323fa3bca"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--70205e3e-195d-4bd5-a208-ada6cdf143e3",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "targets",
      "source_ref": "campaign--d02a1560-ff69-49f4-ac34-919b8aa4b91e",
      "target_ref": "vulnerability--2b7f00d8-b133-4a92-9118-46ce5f8b2531"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--6bb5a995-b874-4e17-88eb-38e00c8e5740",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "targets",
      "source_ref": "campaign--d02a1560-ff69-49f4-ac34-919b8aa4b91e",
      "target_ref": "vulnerability--4d7dc9cb-983f-40b4-b597-d7a38b2d9a4b"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--d4247377-5302-4ede-a0f2-579f7db67bb6",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "targets",
      "source_ref": "campaign--d02a1560-ff69-49f4-ac34-919b8aa4b91e",
      "target_ref": "vulnerability--8323404c-1fdd-4272-822b-829f85556c53"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--b8617e55-00c0-4066-8222-927846edcafe",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--d02a1560-ff69-49f4-ac34-919b8aa4b91e",
      "target_ref": "malware--dc669921-4a1a-470d-bfae-694e740ce181"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--f34d9e2e-715f-4baf-8226-40abfcb91012",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--d02a1560-ff69-49f4-ac34-919b8aa4b91e",
      "target_ref": "malware--f86febd3-609b-4d2e-9fec-aa805cb498bf"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--937f310a-396a-403f-bb6f-400ad8920018",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--4e11b23f-732b-418e-b786-4dbf65459d50",
      "target_ref": "campaign--d02a1560-ff69-49f4-ac34-919b8aa4b91e"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--14a06709-3c0b-4e72-ad49-dd0f6d775e65",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--4e11b23f-732b-418e-b786-4dbf65459d50",
      "target_ref": "malware--dc669921-4a1a-470d-bfae-694e740ce181"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--5f6c6509-ca0c-43db-8c0e-8e138f6d913c",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--b7fa7e73-e645-4813-9723-161bbd8dda62",
      "target_ref": "campaign--d02a1560-ff69-49f4-ac34-919b8aa4b91e"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--ca99fa83-0d1b-4ddd-88c8-0dee38856a88",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--b7fa7e73-e645-4813-9723-161bbd8dda62",
      "target_ref": "malware--f86febd3-609b-4d2e-9fec-aa805cb498bf"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--38a52125-130f-4ce7-9b38-f234553ba83d",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--80c260d9-a075-4148-9301-ebe4af27f449"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--e13b17d0-1fef-4f98-a4a8-895c3e4cf1e2",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--b2f09ce0-2db4-480f-bd2f-073ddb3a0c87",
      "target_ref": "malware--80c260d9-a075-4148-9301-ebe4af27f449"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--262a8234-d7e2-477a-baeb-ed65b639e33a",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--b2f09ce0-2db4-480f-bd2f-073ddb3a0c87",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--f4ceabc6-9302-4dc5-9cc1-4d40ef43503c",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "targets",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "vulnerability--717cb1c9-eab3-4330-8340-e4858055aa80"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--56b1023c-9e28-4449-8b4f-bc2adde45e1a",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "targets",
      "source_ref": "attack-pattern--fb6aa549-c94a-4e45-b4fd-7e32602dad85",
      "target_ref": "vulnerability--717cb1c9-eab3-4330-8340-e4858055aa80"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--8997440e-00f5-48e1-8b56-69d3b6f9f1fd",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--9842a3b9-fc5b-44c4-bb48-578cf6f728d9",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--80ac0601-0660-4057-b3b0-dca0fe35a6b4",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--9842a3b9-fc5b-44c4-bb48-578cf6f728d9",
      "target_ref": "malware--3ed0364f-62c8-4ebc-b136-deaf6966880b"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--2583921a-2f02-42c5-bd25-0f37eb2e6ef9",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--3ed0364f-62c8-4ebc-b136-deaf6966880b"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--7231e729-42e3-4f29-ae6f-6d80192c4bd1",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--4e4c4ad7-4909-456a-b6fa-e24a6f682a40",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--201ee2d5-74f4-4beb-b13a-34d948854655",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--9842a3b9-fc5b-44c4-bb48-578cf6f728d9",
      "target_ref": "malware--17099f03-5ec8-456d-a2de-968aebaafc78"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--afee4dc4-7d0e-450d-9164-4429649ab386",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--17099f03-5ec8-456d-a2de-968aebaafc78"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--ed403d0d-b55d-4e78-94d3-4e035a045c39",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--137acf67-cedc-4a07-8719-72759174de3a",
      "target_ref": "malware--17099f03-5ec8-456d-a2de-968aebaafc78"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--4303ebf2-9590-4ec0-a702-e7bfff64bc5f",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--137acf67-cedc-4a07-8719-72759174de3a",
      "target_ref": "malware--3ed0364f-62c8-4ebc-b136-deaf6966880b"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--54f845bb-0967-4c0f-ac8a-8ad4785cbbe6",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--137acf67-cedc-4a07-8719-72759174de3a",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--0bd19ca0-2bbb-4df0-92ec-59a4e9169c64",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--137acf67-cedc-4a07-8719-72759174de3a",
      "target_ref": "malware--e14b6476-40b5-4b0b-bde7-0e856ab00b6c"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--89ddeb74-ea26-44f9-bb6d-3f17c9d4efaa",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--9695dc2f-d92a-4f2b-8b16-b0e21d7c631d",
      "target_ref": "malware--e14b6476-40b5-4b0b-bde7-0e856ab00b6c"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--eb400750-c866-47c3-89a2-fa6d1a90e9e7",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--9695dc2f-d92a-4f2b-8b16-b0e21d7c631d",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--7450856e-051f-4d49-953c-ad24f170af0e",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--e14b6476-40b5-4b0b-bde7-0e856ab00b6c"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--1d6b0425-603d-4217-948a-fabb2a398450",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--7fd865ed-93e9-481f-953b-82ab386190ae",
      "target_ref": "malware--feaf146d-ea67-4eb1-946a-6f352ff79a81"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--1895dd86-dc46-4505-ba62-5724a1df2362",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--7fd865ed-93e9-481f-953b-82ab386190ae",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--a4e0751d-8d59-4447-96ea-3799fecf66d7",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--feaf146d-ea67-4eb1-946a-6f352ff79a81"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--258796f6-e46a-421a-b3f5-7db6114fb2bc",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--e5bc6507-d052-447f-93c7-db7ef32211da",
      "target_ref": "malware--13791e02-6621-45fb-8c10-f6b72e1bf553"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--9431d9f9-6d8b-4373-b42c-172a663391b3",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--e5bc6507-d052-447f-93c7-db7ef32211da",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--07d2f213-1794-483e-b95b-03761826c052",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--13791e02-6621-45fb-8c10-f6b72e1bf553"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--aa430e5b-0519-4e94-bc2c-8836d196acd7",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--fead5c52-9533-405c-b822-a034092a1ba8",
      "target_ref": "malware--703a15a7-eb85-475d-a27a-77d8fcf8f7b9"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--c0786bd4-9c15-48ee-a19e-a9d6aba25d67",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--fead5c52-9533-405c-b822-a034092a1ba8",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--498b9f3b-488b-40d5-aaaf-e67b93c1d92b",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--703a15a7-eb85-475d-a27a-77d8fcf8f7b9"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--d875538e-cc47-4353-a572-2dae27ef0a44",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--9842a3b9-fc5b-44c4-bb48-578cf6f728d9",
      "target_ref": "malware--fade08cb-fa57-485e-97f8-fab5a1bd4460"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--313d56c4-eef9-417e-952d-073690c20ee4",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--fade08cb-fa57-485e-97f8-fab5a1bd4460"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--6b091c0f-a700-4f3e-9d98-0b8abf9a306b",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--405ff732-2c35-4f46-9f78-2a632ce36e03",
      "target_ref": "malware--3050937d-6330-44c7-83ba-8821e1f7e7bd"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--5aff864a-1789-4df2-87fa-03ec43cf4fdd",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--405ff732-2c35-4f46-9f78-2a632ce36e03",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--325ebcb6-723c-4f50-8a32-aca18809e6eb",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--3050937d-6330-44c7-83ba-8821e1f7e7bd"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--0cb9c725-3d55-4165-b2a9-9414d7933987",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--4d58096e-b5c9-47d8-af9a-1af5f4762d6b",
      "target_ref": "malware--9d995717-edc3-4bd8-8554-aecf773bdecc"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--640a0454-57eb-408f-aa13-b5732b4d0b6f",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--4d58096e-b5c9-47d8-af9a-1af5f4762d6b",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--41550302-6e95-4cf6-8d7c-d417a99d98dc",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--9d995717-edc3-4bd8-8554-aecf773bdecc"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--911dcbb0-96f4-4995-9961-5ea4b2fa7ce2",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--9c725598-a160-4e91-8b93-ed0956709892",
      "target_ref": "malware--40e15fa5-df8d-4771-a682-21dab0a024fd"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--7b6ba584-fa87-4a6f-8c21-8123fa88db74",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--9c725598-a160-4e91-8b93-ed0956709892",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--69101c2f-da92-47af-b402-7c60a39a982f",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--40e15fa5-df8d-4771-a682-21dab0a024fd"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--25055108-a2ae-4855-bd5f-6ab396aacbc5",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--2efe7c62-1b96-4568-81ee-c85b840bde39",
      "target_ref": "malware--69101c2f-da92-47af-b402-7c60a39a982f"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--44c80cab-73ce-4b17-a4cb-9a36e2585403",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--2efe7c62-1b96-4568-81ee-c85b840bde39",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--32655cb3-7455-4761-b1f2-0b82153a0540",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--69101c2f-da92-47af-b402-7c60a39a982f"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--fe963c8c-65a4-49ea-910b-e1cf3c80f1b4",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--b8322c9b-8031-4fb3-9cbc-8a1ea0fe3cfa",
      "target_ref": "malware--1601b8c2-5e6f-4a18-a413-10527e5d90b7"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--4b0abf75-6f05-4bd5-8ac5-19778b245274",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--b8322c9b-8031-4fb3-9cbc-8a1ea0fe3cfa",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--154049a5-731d-4e50-af13-f0f2c9b71f91",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--1601b8c2-5e6f-4a18-a413-10527e5d90b7"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--db55db06-499d-4867-9ab9-3ed4331eedb2",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--b08f9631-dd94-4d99-a96c-32b42af2ea81",
      "target_ref": "malware--626badcc-4257-4222-946c-6d6e889836ea"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--cc802697-7677-4bd7-a8b9-e728788ac783",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--b08f9631-dd94-4d99-a96c-32b42af2ea81",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--a371be18-8ca5-4453-80f5-ae52d982c21b",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--626badcc-4257-4222-946c-6d6e889836ea"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--9a3bd620-01b5-4764-beb0-f085417ed8f3",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--137acf67-cedc-4a07-8719-72759174de3a",
      "target_ref": "malware--3b275ed1-9c2e-4443-b1dd-5cfb51eaef2e"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--48906405-9980-4583-8559-2085c111bf89",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--3b275ed1-9c2e-4443-b1dd-5cfb51eaef2e"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--13222c71-d8fa-4688-adae-c3f8ca43a41b",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--137acf67-cedc-4a07-8719-72759174de3a",
      "target_ref": "malware--f138b6e0-9a7d-4cd9-a904-08a7df2eabb1"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--73c4529e-560e-4831-8497-a0db72f7dfd8",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--f138b6e0-9a7d-4cd9-a904-08a7df2eabb1"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--8d3e1ed6-7d9c-4aa5-b121-f4eb193312cf",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--950c01b8-c647-4cc8-b0c1-3612fa780108",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--2c11dcc0-7968-4c07-bdde-791a8f5e2e37",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--302ac5b5-486c-4c99-8cad-4426aeaf47b6"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--fd97d0ef-370e-4b6f-b2d3-8fb881aadc3f",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--950c01b8-c647-4cc8-b0c1-3612fa780108",
      "target_ref": "malware--302ac5b5-486c-4c99-8cad-4426aeaf47b6"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--c05d2410-848c-47e5-a94f-c64510e2b08d",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--ae29faa6-5f70-4eb8-981b-30818433a52e",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--92a21b52-2961-42aa-8b01-54ea294d9d73",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--e1c02dca-d3fe-48f1-bb4b-3cacd2bc3619"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--76a9283a-b844-47a5-a5d0-b31859115f88",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--ae29faa6-5f70-4eb8-981b-30818433a52e",
      "target_ref": "malware--e1c02dca-d3fe-48f1-bb4b-3cacd2bc3619"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--bbd3ba5c-2a75-4902-bd42-1215a2bc320e",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--137acf67-cedc-4a07-8719-72759174de3a",
      "target_ref": "malware--e1c02dca-d3fe-48f1-bb4b-3cacd2bc3619"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--4f784f2f-7d8e-4f12-9ddd-b685055f8076",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--b6cc482d-89db-4e6b-a592-723070f6d22d",
      "target_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--263e38f4-8ecb-414f-b3c4-0f045d1be5ed",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "uses",
      "source_ref": "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
      "target_ref": "malware--a4f315bd-e159-4bfb-8439-0d5a8330fc70"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--a56e8582-fc6e-4be8-bf35-7e939269d65e",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--b6cc482d-89db-4e6b-a592-723070f6d22d",
      "target_ref": "malware--a4f315bd-e159-4bfb-8439-0d5a8330fc70"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--d7d9952c-4443-4711-a48c-7009a0f0f8ea",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--137acf67-cedc-4a07-8719-72759174de3a",
      "target_ref": "malware--a4f315bd-e159-4bfb-8439-0d5a8330fc70"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--78f110e6-2cd6-442e-971f-a2ff40c3b843",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--0b71628d-31dd-4eb8-baee-39f19c0a14b0",
      "target_ref": "malware--40e15fa5-df8d-4771-a682-21dab0a024fd"
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--b2fb88f2-5ad7-4c07-b4b2-61986decb477",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--0b71628d-31dd-4eb8-baee-39f19c0a14b0",
      "target_ref": "malware--69101c2f-da92-47af-b402-7c60a39a982f"
    }
  ]
}
"""

bundle = json.loads(bundle)
objects = bundle.get("objects")
raw_indicators = []
for object in objects:
    if object.get("type") == "indicator":
        raw_indicators.append(object)

indicators = []
for raw_indicator in raw_indicators:
    indicator = Indicator(
        # uuid=uuid.uuid5(),
        value=raw_indicator.get("name"),
        first_detected_date=raw_indicator.get("created"),
        updated_date=raw_indicator.get("modified"),
    )
    pattern = raw_indicator.get("pattern")
    if "ip" in pattern:
        indicator.ioc_context_ip = pattern
    elif "filesize" in pattern:
        indicator.ioc_context_file_size = pattern

    indicators.append(indicator)
