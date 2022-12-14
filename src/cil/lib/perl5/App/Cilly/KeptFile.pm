package App::Cilly::KeptFile;

use App::Cilly::OutputFile;
our @ISA = (App::Cilly::OutputFile);

use strict;
use Carp;
use File::Basename;
use File::Spec;


########################################################################


sub new {
    croak 'bad argument count' unless @_ == 4;
    my ($proto, $basis, $suffix, $dir) = @_;
    my $class = ref($proto) || $proto;

    $basis = $basis->basis if ref $basis;
    my ($basename, undef, $basefix) = fileparse($basis, qr{\.[^.]+});
    my $filename = File::Spec->catfile($dir, "$basename.$suffix");

    my $self = $class->SUPER::new($basis, $filename);
    return $self;
}


########################################################################


1;

__END__


=head1 Name

KeptFile - persistent compiler output files

=head1 Synopsis

    use KeptFile;

    my $cppOut = new KeptFile ('code.c', 'i', '/output/directory');
    system 'cpp', 'code.c', '-o', $cppOut->filename;

=head2 Description

C<KeptFile> represents an intermediate output file generated by some
stage of a C<Cilly>-based compiler that should be retained after
compilation.  It is a concrete subclass of L<OutputFile|OutputFile>.
Use C<KeptFile> when the user has asked for intermediate files to be
retained, such as via gcc's C<-save-temps> flag.

=head2 Public Methods

=over

=item new

C<new KeptFile ($basis, $suffix, $dir)> constructs a new C<KeptFile>
instance.  The new file name is constructed using the base file name
of C<$basis> with its suffix replaced by C<$suffix> and its path given
by C<$dir>.  For example,

    new KeptFile ('/foo/code.c', 'i', '/bar')

yields a C<KeptFile> with file name F</bar/code.i>.

C<$basis> may be either absolute or relative; only the trailing file
name is used.  C<$basis> can also be an C<OutputFile> instance, in
which case C<< $basis->basis >> is used as the actual basis.  See
L<OutputFile/"basis"> for more information on basis flattening.

C<$suffix> should not include a leading dot; this will be added
automatically.

C<$dir> may be either absolute or relative.  It is common to use F<.>
as the directory, which puts the C<KeptFile> in the current working
directory.

=back

=head1 See Also

L<OutputFile>, L<TempFile>.

=cut
