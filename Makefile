microtest:
	python $$CODEBASE/ATACseq/pipelines/ATACseq.py -I $$MICROTEST/data/atacR1.fq.gz -I2 $$MICROTEST/data/atacR2.fq.gz -G hg19 -O $$HOME/scratch -S atac_test --single-or-paired paired -R
test:
	python pipelines/ATACseq.py  -P 3 -M 100 -O test_out -R -S liver -G hg19  -Q paired  -C ATACseq.yaml  --genome-size hs --prealignments rCRSd human_repeats -I examples/test_data/liver-CD31_test_R1.fastq.gz -I2 examples/test_data/liver-CD31_test_R2.fastq.gz  
changtest:
	python pipelines/ATACseq.py  -P 3 -M 100 -O test_out -R -S liver -G hg19  -Q paired  -C $HOME/code/ATACseq/examples/chang_project/ATACseq.yaml  -gs mm -I examples/test_data/liver-CD31_test_R1.fastq.gz -I2 examples/test_data/liver-CD31_test_R2.fastq.gz 


docker:
	docker build -t databio/pepatac -f containers/pepatac.Dockerfile .

singularity:
	singularity build $${SIMAGES}pepatac docker://databio/pepatac