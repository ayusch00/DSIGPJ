import os
import subprocess

def run_java_command():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    snpEff_jar_path = os.path.join(script_dir, 'snpEff', 'snpEff.jar')
    snpEff_config_path = os.path.join(script_dir, 'snpEff', 'snpEff.config')
    vcf_path = os.path.join(script_dir, 'data', 'test.vcf')
    output_file_path = os.path.join(script_dir, 'data', 'test.ann.vcf')

    command = f"java -Xmx4g -jar \"{snpEff_jar_path}\" -c \"{snpEff_config_path}\" GRCh37.75 \"{vcf_path}\" > \"{output_file_path}\""

    print(command)
    process = subprocess.run(command, shell=True, capture_output=True, text=True)

    if process.stderr:
        print(f"Error: {process.stderr}")
    else:
        print(f"Output: {process.stdout}")

# usage
run_java_command()

def run_java_command2():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    snpSift_jar_path = os.path.join(script_dir, 'snpEff', 'SnpSift.jar')
    vcf_path = os.path.join(script_dir, 'data', 'clinvar.vcf')
    vcf_annotation_path = os.path.join(script_dir, 'data', 'test.ann.vcf')
    output_file_path = os.path.join(script_dir, 'data', 'clinvar.ann.vcf')

    command = f"java -jar \"{snpSift_jar_path}\" annotate \"{vcf_path}\" \"{vcf_annotation_path}\" > \"{output_file_path}\""

    print(command)
    process = subprocess.run(command, shell=True, capture_output=True, text=True)

    if process.stderr:
        print(f"Error: {process.stderr}")
    else:
        print(f"Output: {process.stdout}")

run_java_command2()