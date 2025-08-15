from __future__ import annotations
import botocore
import boto3

def ensure_stack(region: str, stack_name: str, template_body: str, params: dict, tags: dict):
    cf = boto3.client("cloudformation", region_name=region)
    parameters = [{"ParameterKey": k, "ParameterValue": str(v)} for k, v in params.items() if v is not None]
    tag_list = [{"Key": k, "Value": str(v)} for k, v in (tags or {}).items()]

    try:
        print(f"Creating stack {stack_name} in {region} ...")
        cf.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=parameters,
            Capabilities=["CAPABILITY_NAMED_IAM"],
            Tags=tag_list,
        )
        waiter = cf.get_waiter("stack_create_complete")
        waiter.wait(StackName=stack_name)
        print("Create complete.")
    except botocore.exceptions.ClientError as e:
        msg = str(e)
        if "AlreadyExistsException" in msg or "already exists" in msg.lower():
            print(f"Updating stack {stack_name} ...")
            try:
                cf.update_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Parameters=parameters,
                    Capabilities=["CAPABILITY_NAMED_IAM"],
                    Tags=tag_list,
                )
                waiter = cf.get_waiter("stack_update_complete")
                waiter.wait(StackName=stack_name)
                print("Update complete.")
            except botocore.exceptions.ClientError as ue:
                if "No updates are to be performed" in str(ue):
                    print("No updates to perform.")
                else:
                    raise
        else:
            raise

def stack_status(region: str, stack_name: str) -> dict:
    cf = boto3.client("cloudformation", region_name=region)
    try:
        resp = cf.describe_stacks(StackName=stack_name)
        stack = resp["Stacks"][0]
        outputs = {o["OutputKey"]: o["OutputValue"] for o in stack.get("Outputs", [])}
        return {
            "StackName": stack["StackName"],
            "Status": stack["StackStatus"],
            "CreationTime": str(stack["CreationTime"]),
            "LastUpdatedTime": str(stack.get("LastUpdatedTime", "")),
            "Outputs": outputs,
        }
    except botocore.exceptions.ClientError as e:
        if "does not exist" in str(e):
            return {"error": f"Stack {stack_name} not found."}
        raise

def destroy_stack(region: str, stack_name: str):
    cf = boto3.client("cloudformation", region_name=region)
    print(f"Deleting stack {stack_name} ...")
    cf.delete_stack(StackName=stack_name)
    waiter = cf.get_waiter("stack_delete_complete")
    waiter.wait(StackName=stack_name)
    print("Delete complete.")
