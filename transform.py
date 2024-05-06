import os
import vcf
import pandas as pd

# Load VCF file using PyVCF
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, 'data', 'clinvar.ann.vcf')
vcf_reader = vcf.Reader(open(file_path, 'r'))


# Prepare DataFrame to hold the ChromosomeSequence data
chromosome_sequences = pd.DataFrame(columns=['chromosome', 'assembly'])

# Determine the assembly from VCF metadata if available
# This is an assumption, replace 'GRCh38' with actual data if available from your VCF meta-information
default_assembly = 'GRCh38'

# Extract ChromosomeSequence data
for record in vcf_reader:
    chromosome_sequences = chromosome_sequences.append({
        'chromosome': record.CHROM,
        'assembly': default_assembly  # Assuming all records are from the same assembly
    }, ignore_index=True)

# Remove duplicates if any, since many records will have the same chromosome and assembly
chromosome_sequences.drop_duplicates(inplace=True)

# Save to CSV
output_file_path = os.path.join(script_dir, 'csvFiles', 'ChromosomeSequence.csv')
chromosome_sequences.to_csv(output_file_path, index=False)

# Prepare DataFrame to store the annotation data
annotations = pd.DataFrame(columns=['impact', 'consequence', 'allele'])

vcf_reader = vcf.Reader(open(file_path, 'r'))
for record in vcf_reader:
    if 'ANN' in record.INFO:
        # The ANN field is already a list of annotations
        for ann in record.INFO['ANN']:
            # Each 'ann' is a string of annotations details separated by '|'
            parts = ann.split('|')
            if len(parts) >= 16:  # Ensure there are enough parts to extract needed information
                allele = parts[0].strip()
                consequence = parts[1].strip()
                impact = parts[2].strip()

                # Append the extracted data to the DataFrame
                annotations = annotations.append({
                    'impact': impact,
                    'consequence': consequence,
                    'allele': allele
                }, ignore_index=True)

# Remove duplicates from the DataFrame
annotations = annotations.drop_duplicates()

# Save the data to a CSV file
output_file_path = os.path.join(script_dir, 'csvFiles', 'Annotations.csv')
annotations.to_csv(output_file_path, index=False)

# Function to determine variant type based on REF and ALT alleles
def determine_variant_type(ref, alt):
    if len(ref) == 1 and len(alt) == 1:
        return 'SNP'
    elif len(ref) > len(alt):
        return 'deletion'
    elif len(ref) < len(alt):
        return 'insertion'
    else:
        return 'complex'

# Load VCF file using PyVCF
vcf_reader = vcf.Reader(open(file_path, 'r'))

# List to hold variant data
variant_data = []

# Extract variant information
for record in vcf_reader:
    variant_rs_id = record.ID
    ref = record.REF
    alt = ','.join([str(a) for a in record.ALT])  # Join all ALT alleles into a string
    variant_type = determine_variant_type(ref, record.ALT[0])

    # Append variant information as a dictionary
    variant_data.append({
        'variant_rs_id': variant_rs_id,
        'ref': ref,
        'alt': alt,
        'variant_type': variant_type
    })

# Convert list to DataFrame
variants_df = pd.DataFrame(variant_data)

# Save DataFrame to CSV
output_file_path = os.path.join(script_dir, 'csvFiles', 'variants.csv')
variants_df.to_csv(output_file_path, index=False)

# Function to parse HGVS notations from an annotation string
def parse_hgvs(annotations):
    hgvs_c = []
    hgvs_p = []
    for ann in annotations:
        parts = ann.split('|')
        if len(parts) > 10:  # Ensuring there are enough parts
            hgvs_c_value = parts[9].strip()  # HGVS.c value
            hgvs_p_value = parts[10].strip()  # HGVS.p value
            if hgvs_c_value:  # Only add if there is a value
                hgvs_c.append(hgvs_c_value)
            if hgvs_p_value:  # Only add if there is a value
                hgvs_p.append(hgvs_p_value)
    return hgvs_c, hgvs_p

# Load VCF file using PyVCF
vcf_reader = vcf.Reader(open(file_path, 'r'))

# Prepare DataFrame to hold the HGVS expressions
hgvs_expressions = pd.DataFrame(columns=['hgvs_c', 'hgvs_p'])

# Extract HGVS data
for record in vcf_reader:
    if 'ANN' in record.INFO:
        hgvs_c_list, hgvs_p_list = parse_hgvs(record.INFO['ANN'])
        for hgvs_c, hgvs_p in zip(hgvs_c_list, hgvs_p_list):
            hgvs_expressions = hgvs_expressions.append({
                'hgvs_c': hgvs_c,
                'hgvs_p': hgvs_p
            }, ignore_index=True)

# Remove duplicates if any
hgvs_expressions.drop_duplicates(inplace=True)

# Save to CSV
output_file_path = os.path.join(script_dir, 'csvFiles', 'HGVSExpressions.csv')
hgvs_expressions.to_csv(output_file_path, index=False)

##############################################################################################################

def parse_diseases(clndn_info_list):
    diseases = []
    for clndn_info in clndn_info_list:
        # Assuming that each entry might still contain multiple diseases separated by '|'
        diseases.extend(clndn_info.split('|'))
    return diseases

# Load VCF file using PyVCF
vcf_reader = vcf.Reader(open(file_path, 'r'))

# Prepare DataFrame to hold the Disease data
diseases = pd.DataFrame(columns=['preferred_name'])

# Example usage within the main script
for record in vcf_reader:
    if 'CLNDN' in record.INFO:
        disease_list = parse_diseases(record.INFO['CLNDN'])  # This now expects a list
        for disease in disease_list:
            diseases = diseases.append({'preferred_name': disease}, ignore_index=True)

# Remove duplicates if any
#diseases.drop_duplicates(inplace=True)

# Save to CSV
output_file_path = os.path.join(script_dir, 'csvFiles', 'Diseases.csv')
diseases.to_csv(output_file_path, index=False)

##############################################################################################################

# Function to extract interpretation details from the record
def parse_interpretation(info):
    # Extract relevant fields from INFO, provide defaults if not present
    clinical_significance = info.get('CLNSIG', 'Not provided')
    review_status = info.get('CLNREVSTAT', 'Not reviewed')
    method = info.get('METHOD', 'Unknown method')  
    variant_origin = info.get('ORIGIN', 'Unknown origin')  
    return clinical_significance, review_status, method, variant_origin

# Load VCF file using PyVCF
vcf_reader = vcf.Reader(open(file_path, 'r'))

# Prepare DataFrame to hold the Interpretation data
interpretations = pd.DataFrame(columns=['clinical_significance', 'review_status', 'method', 'variant_origin'])

# Extract interpretation data
for record in vcf_reader:
    if any(tag in record.INFO for tag in ['CLNSIG', 'CLNREVSTAT', 'METHOD', 'ORIGIN']):  
        clinical_significance, review_status, method, variant_origin = parse_interpretation(record.INFO)
        interpretations = interpretations.append({
            'clinical_significance': clinical_significance,
            'review_status': review_status,
            'method': method,
            'variant_origin': variant_origin
        }, ignore_index=True)

# Remove duplicates if any
#interpretations.drop_duplicates(inplace=True)

# Save to CSV
output_file_path = os.path.join(script_dir, 'csvFiles', 'Interpretations.csv')
interpretations.to_csv(output_file_path, index=False)

##############################################################################################################

database_urls = {
    'dbSNP': 'https://www.ncbi.nlm.nih.gov/snp/',
    'ClinVar': 'https://www.ncbi.nlm.nih.gov/clinvar/',
    'dbVar': 'https://www.ncbi.nlm.nih.gov/dbvar/',
    'ExAC': 'http://exac.broadinstitute.org/'
}

def get_database_info(record):
    databases = []
    # Check if 'RS' exists and handle it as a list
    if 'RS' in record.INFO:
        rs_ids = record.INFO['RS']  # Assuming it's already a list
        for rs_id in rs_ids:
            # Check if rs_id is a string and construct the URL
            if isinstance(rs_id, str):
                databases.append(('dbSNP', f"{database_urls['dbSNP']}{rs_id}"))
            elif isinstance(rs_id, int):  # Sometimes rs numbers are integers
                databases.append(('dbSNP', f"{database_urls['dbSNP']}rs{rs_id}"))
    if 'CLNVI' in record.INFO:
        # Example to handle potentially single value or list
        clnvi_ids = record.INFO['CLNVI']
        if isinstance(clnvi_ids, list):
            for clnvi_id in clnvi_ids:
                databases.append(('ClinVar', f"{database_urls['ClinVar']}{clnvi_id}"))
        else:
            databases.append(('ClinVar', f"{database_urls['ClinVar']}{clnvi_ids}"))

    return databases


# Path setup
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, 'data', 'clinvar.ann.vcf')

# DataFrame setup
databases_df = pd.DataFrame(columns=['Name', 'URL'])

# Parsing VCF
for record in vcf_reader:
    for name, url in get_database_info(record):
        databases_df = databases_df.append({'Name': name, 'URL': url}, ignore_index=True)

# Drop duplicates and save to CSV
output_file_path = os.path.join(script_dir, 'csvFiles',  'Databases.csv')
#databases_df.drop_duplicates(inplace=True)
databases_df.to_csv(output_file_path, index=False)

##############################################################################################################

def get_disease_and_interpretation_info(record):
    # Extract disease and interpretation info
    disease_name = record.INFO.get('CLNDN', 'Unknown Disease')  # Use actual INFO tag names from your VCF
    clinical_significance = record.INFO.get('CLNSIG', 'Not specified')
    review_status = record.INFO.get('CLNREVSTAT', 'Not reviewed')
    return disease_name, clinical_significance, review_status

# Assuming file_path is already set up and points to the 'clinvar.ann.vcf'
vcf_reader = vcf.Reader(open(file_path, 'r'))

# DataFrame to hold the relationship data
relationships = pd.DataFrame(columns=['Disease', 'Clinical Significance', 'Review Status'])

# Parse the VCF file
for record in vcf_reader:
    disease_name, clinical_significance, review_status = get_disease_and_interpretation_info(record)
    relationships = relationships.append({
        'Disease': disease_name,
        'Clinical Significance': clinical_significance,
        'Review Status': review_status
    }, ignore_index=True)

# Remove duplicates
#relationships.drop_duplicates(inplace=True)

# Save to CSV
output_file_path = os.path.join('csvFiles', 'ForA.csv')
relationships.to_csv(output_file_path, index=False)

##############################################################################################################

# Assuming file_path and vcf.Reader are properly set
vcf_reader = vcf.Reader(open(file_path, 'r'))

# DataFrame to hold the relationship data
located_in = pd.DataFrame(columns=['Chromosome', 'Assembly', 'Position', 'Reference'])

# Default assembly, if not specified in the VCF file
default_assembly = 'GRCh38'  # Adjust this as needed based on your VCF file specifics

# Parse the VCF file
for record in vcf_reader:
    located_in = located_in.append({
        'Chromosome': record.CHROM,
        'Assembly': default_assembly,  # You might extract this dynamically if available
        'Position': record.POS,
        'Reference': record.REF
    }, ignore_index=True)

# Remove duplicates if any
#located_in.drop_duplicates(inplace=True)

# Save to CSV
output_file_path = os.path.join('csvFiles', 'Located_In_Relationship.csv')
located_in.to_csv(output_file_path, index=False)