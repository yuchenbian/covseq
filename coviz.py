import click
from datetime import date
import time
from annotate import annotate
from orf_prediction import predict
@click.group()
def coviz():
	pass

@coviz.command()
@click.option("-f", "--fasta", type=str, required=True, \
	help="Fasta file containing one or more virus strains.")
@click.option("-o", "--out_dir", type=str, required=False, \
	help="Output directory", default="results", show_default=True)
def annotate_interface(fasta, out_dir):
	click.echo(f"FASTA file: {fasta}")
	click.echo(f"Output directory: {out_dir}")
	annotate(fasta, out_dir)

@coviz.command()
@click.option("-f", "--fasta", type=str, required=True, \
	help="Fasta file containing one or more virus strains.")
@click.option("-o", "--out_dir", type=str, required=False, \
	help="Output directory", default="results", show_default=True)
def predict_inferface():
	click.echo(f"FASTA file: {fasta}")
	click.echo(f"Output directory: {out_dir}")
	predict(fasta, out_dir)


# @coviz.command()
# def phylogeny():
# 	pass


if __name__ == "__main__":
	coviz()