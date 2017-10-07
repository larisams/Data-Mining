# ============================================================================================
# >>>>>>>>>>>>>>>>>>>>>>>>>>>> Phenotype Tagging <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# AUTHOR : Maria Jose Rocha Acevedo
# VERSION: 1.0
# CREATED: 18/09/2017 10:55 pm
# DESCRIPTION: This program locates phenotype (medical condition) names and adds tags around 
# the name's appearance in the input text in order to ease its later identification.
# After that, it tags the rs IDs present in the file 
# USAGE : This program requires a text file with a list of phenotype names (each of which must 
# be on a single line) and a separate file with the text where the phenotype names will be located. 
# It prints the output to stdout
# REQUIREMENTS : Flat text input files, paths must be added directly to the code
# CATEGORY : Standalone
# INPUT FORMAT : Flat text
# OUTPUT FORMAT : The output resembles the input file including the text where the phenotype 
# names are located, including the added tags (<PHE>phenotype name</PHE>)
# LANGUAGE : Perl
# PATH PROGRAM : /export/storage/users/mrocha/Tagging/EnfTags.pl
# =============================================================================================

#!/usr/bin/perl
open(ABST, "/Files/TaggedAbstracts.txt") or die "AbstractFile not found";
$count=0;
while (<ABST>){
	open(DICT, "dic_enf_gs.txt") or die "Dictionary not found";
        unless($count){
                $line=$_;
        }
	for (<DICT>){
		chomp;
		$enf=$_;
		if ($line=~/\s+\b($enf)\b[\s+|\.]/ig){
			$line=~s/($enf)/\<PHE\>$1\<\/PHE\>/ig;
			$count+=1;
		}
	}
	print "$line\n";
	$count=0;
}

# Tagging RS in all abstracts
# Tag = <RS> [RSnumber] </RS>

perl -ne 'chomp;$line=$_;if (/(rs\d+)/){$rs=$1}; $line=~ s/rs\d+/\<RS\>$rs\<\/RS\>/g; print "$line\n";' /export/storage/users/mrocha/Tagging/nohup.out > /home/larisams/storage/BEI_project/data_source/All_abstract_Tagged_RS_PHEN.txt
