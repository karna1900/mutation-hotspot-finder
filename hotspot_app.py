# 🔥 Hotspot Finder App
# Made by: Aakash Karna

import streamlit as st
import pandas as pd
from Bio import SeqIO
import io

# Page settings
st.set_page_config(page_title="Mutation Hotspot Finder", layout="centered")

# ====================== UI Part ======================

# Title
st.title("🧬 Mutation Hotspot Finder")

# About Section
st.markdown("""
Welcome to the **Mutation Hotspot Finder**!  
This tool allows researchers to upload a reference genome (FASTA format) and a somatic mutation matrix (CSV format),  
and quickly detect **mutation hotspots** — regions in the genome frequently affected by mutations.  
Designed to make hotspot detection super simple and accessible! 🚀
""")

# FAQ Section
st.header("❓ FAQ")

with st.expander("What is a mutation hotspot?"):
    st.write("A mutation hotspot is a region in the genome where mutations happen frequently, often linked to diseases like cancer.")

with st.expander("What file formats are supported?"):
    st.write("Supported formats: .fna, .fasta (for genome) and .csv (for mutations matrix).")

with st.expander("Is this tool free to use?"):
    st.write("Yes! 100% free and open for educational and research purposes.")

# ====================== Upload & Processing Part ======================

st.write("---")  # a nice divider

# File uploads
ref_file = st.file_uploader("📄 Upload Reference Genome (FASTA format)", type=["fna", "fasta"])
mutation_file = st.file_uploader("📄 Upload Mutations Matrix (CSV format)", type=["csv"])

if ref_file and mutation_file:
    try:
        # Load reference genome
        ref_text = ref_file.read().decode('utf-8')
        ref_sequences = SeqIO.to_dict(SeqIO.parse(io.StringIO(ref_text), "fasta"))

        # Load mutation matrix
        mutations_df = pd.read_csv(mutation_file, index_col=0)

        st.success("✅ Files loaded successfully!")

        # Detect hotspots
        st.subheader("🔎 Detecting Hotspots...")
        results = []

        for gene in mutations_df.columns:
            mutation_counts = mutations_df[gene]
            total_mutations = mutation_counts.sum()

            if int(total_mutations) > 0:
                results.append({
                    "Gene": gene,
                    "Total_Mutations": int(total_mutations)
                })

        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values(by="Total_Mutations", ascending=False)

        st.success("✅ Hotspot Detection Completed!")

        # Show top hotspots
        st.subheader("🔥 Top Hotspots Found")
        st.dataframe(results_df)

        # Download button
        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Results as CSV",
            data=csv,
            file_name='HotspotResults.csv',
            mime='text/csv',
        )

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")

# ====================== Footer Part ======================

st.markdown("---")
st.markdown("""
<center>
<h5>Built with ❤️ by Aakash Karna</h5>
<p>Contact: <a href="https://www.linkedin.com/in/aakash-karna-59b79b273?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" target="_blank">LinkedIn</a></p>
</center>
""", unsafe_allow_html=True)
